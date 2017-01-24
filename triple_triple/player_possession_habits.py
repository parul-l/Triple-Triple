from triple_triple.team_shooting_side import get_initial_shooting_sides

from triple_triple.config import DATASETS_DIR
from triple_triple.court_regions import get_region

from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play


from triple_triple.startup_data import (
    get_df_play_by_play,
    get_df_raw_position_data,
    get_game_info_dict
)

df_raw_position_data = get_df_raw_position_data()
df_play_by_play = get_df_play_by_play()
game_info_dict = get_game_info_dict()
df_game_stats = parse_df_play_by_play(df_play_by_play)


initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_raw_position_data, game_info_dict)


def get_possession_df(df_raw_position_data, has_ball_dist=2.0, len_poss=25):
    df_possession = df_raw_position_data.query('closest_to_ball==True and dist_to_ball<=@has_ball_dist').reset_index(drop=True)

    # determine where player_ids change
    idx_poss_change = np.where(df_possession.player_id.values[:-1] != df_possession.player_id.values[1:])[0]

    # length of consecutive player
    idx_diff = idx_poss_change[1:] - idx_poss_change[:-1]

    # idices where length is >= len_poss
    idx_of_poss = np.where(idx_diff >= len_poss)[0]

    # add possession column
    df_possession['possession'] = None

    for idx in idx_of_poss:
        df_possession.possession.loc[idx_poss_change[idx] + 1] = 'Start'
        df_possession.possession.loc[idx_poss_change[idx + 1]] = 'Stop'
        
        df_possession.possession.loc[idx_poss_change[idx] + 2:idx_poss_change[idx + 1] - 1] = True

    return df_possession[df_possession.possession.notnull()]


def get_court_region(dataframe_row, initial_shooting_side):
    period, team_id, x, y = dataframe_row[0], dataframe_row[1], dataframe_row[2], dataframe_row[3]

    if team_id != -1:
        if period == 1 or period == 3:
            shooting_side = initial_shooting_side[team_id]
            return get_region(x, y, shooting_side)
        if period == 2 or period == 4:
            # switch sides
            teams = initial_shooting_side.keys()
            initial_shooting_side[teams[0]], initial_shooting_side[teams[1]] = initial_shooting_side[teams[1]], initial_shooting_side[teams[0]]
            shooting_side = initial_shooting_side[team_id]
            return get_region(x, y, shooting_side)


def add_regions_to_df(df_possession):
    df_select = df_possession[['period', 'team_id', 'x_loc', 'y_loc']]
    regions_array = df_select.apply(get_court_region, axis=1)
    df_possession['region'] = regions_array

    return df_possession


def add_empty_action_to_df_raw(df_possession):
    df_possession['action'] = None

    return df_possession


def update_df_possession_action(end_poss_idx, action, df_possession_action):
    df_possession_action.action.loc[end_poss_idx] = action
    return df_possession_action


def check_action(game_clock_tuple, df_game_player, action, time_error):
    start_game_clock = game_clock_tuple[0]
    end_game_clock = game_clock_tuple[1]

    if action == "shot":
        df_game_player_action_gc = df_game_player.query('action==@action or action=="missed_shot"').game_clock.values
    else:
        df_game_player_action_gc = df_game_player.query('action==@action').game_clock.values

    if any(end_game_clock - time_error <= gc <= start_game_clock for gc in df_game_player_action_gc):
        return True
    else:
        return False


def characterize_possession_to_player(game_id, player_id, df_possession_action, df_game_stats):

    grouped_poss_df = df_possession_action.groupby(['game_id', 'player_id'])

    df_player_poss = grouped_poss_df.get_group((game_id, player_id)).query('possession=="Start" or possession=="Stop"')

    # characterize each possession
    
    for i in range(0, len(df_player_poss), 2):
        period = df_player_poss.period.iloc[i]
        game_clock_start = df_player_poss.game_clock.iloc[i]
        game_clock_end = df_player_poss.game_clock.iloc[i + 1]

        end_poss_idx = df_player_poss.index[i + 1]

        df_game_player = df_game_stats.query('game_id==@game_id and player_id==@player_id and period==@period')

        # check shot
        if check_action(
            game_clock_tuple=(game_clock_start, game_clock_end),
            df_game_player=df_game_player,
            action='shot',
            time_error=2
        ):
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='shot',
                df_possession_action=df_possession_action
            )

        # check turnover
        elif check_action(
            game_clock_tuple=(game_clock_start, game_clock_end),
            df_game_player=df_game_player,
            action="turnover",
            time_error=2
        ):
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='turnover',
                df_possession_action=df_possession_action
            )

        # deduce pass
        else:
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='pass',
                df_possession_action=df_possession_action,
            )

    return df_possession_action







#####################
##### OLD ONE #######
#####################
import cPickle as pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from triple_triple.team_shooting_side import (
    team_id_from_name,
    team_shooting_side
)
from triple_triple.config import DATASETS_DIR
from triple_triple.court_regions import region
from triple_triple.data_generators.player_game_stats_data import (
    player_team_loc_from_name,
    player_impact_df,
    player_game_stats_nba
)

# TODO: Change get_known_player_possession so that input dataframe is df_pos_dist_reg_trunc (not df_pos_dist)

# player_court_region determines player's region every moment he is on the court
# and hence uses df_pos_dist

# player possession functions use df_pos_dist_trunc, which considers
# players closest to ball when dist < 2

# has_ball_dist dist set to same dist used in get_df_pos_dist_trunc


def get_pos_trunc_df(df_pos, has_ball_dist=2):
    return df_pos[df_pos['min_dist'].values < has_ball_dist].reset_index()


def get_player_court_region_df(
    df_pos_dist, initial_shooting_side,
    hometeam_id, awayteam_id
):
    period_list = df_pos_dist.period.values.flatten()
    df_pos_x_loc = df_pos_dist.iloc[:, df_pos_dist.columns.
                                    get_level_values(1) == 'x_loc'].values
    df_pos_y_loc = df_pos_dist.iloc[:, df_pos_dist.columns.
                                    get_level_values(1) == 'y_loc'].values

    # get column headers = player list
    # (Note: df_pos_dist.columns.levels[0] doesn't preserve the order of the columns)
    player_list = list(df_pos_dist)[:78:3]
    player_list = map(lambda x: x[0], player_list)

    for j in range(len(player_list)):
        player_court_region = [None] * len(df_pos_x_loc)
        for i in range(len(df_pos_x_loc)):
            shooting_side = team_shooting_side(
                player_list[j],
                period_list[i],
                initial_shooting_side,
                hometeam_id,
                awayteam_id
            )
            if not np.isnan(df_pos_x_loc[i, j]):
                player_court_region[i] = region(
                    df_pos_x_loc[i, j],
                    df_pos_y_loc[i, j],
                    shooting_side
                )
        df_pos_dist[player_list[j], 'region'] = player_court_region

    return df_pos_dist.sort_index(axis=1)


def player_possession_idx(player, df_pos_dist_reg_trunc):
    closest_player_to_ball = df_pos_dist_reg_trunc.closest_player.values.flatten()

    player_ball = [None] * len(closest_player_to_ball)
    next_player_ball = [None] * len(closest_player_to_ball)

    player_ball_idx = []
    next_player_ball_idx = []

    # track the start and end of possessions
    for i in range(len(closest_player_to_ball)):
        if (closest_player_to_ball[i] == player and
                closest_player_to_ball[i - 1] != player):

            player_ball[i] = player
            player_ball_idx.append(i)
        elif (closest_player_to_ball[i] != player and
                closest_player_to_ball[i - 1] == player):

            next_player_ball[i] = closest_player_to_ball[i]
            next_player_ball_idx.append(i)

    return [
        player_ball,
        next_player_ball,
        player_ball_idx,
        next_player_ball_idx
    ]


def shot_made_or_miss(shoot_list):
    if shoot_list[0] == 'MISS':
        return 0
    elif '3PT' in shoot_list:
        return 3
    else:
        return 2


def get_possession_list(
    type_poss_list,
    period_play_start,
    game_clock_play_end,
    time,
    start_region,
    end_region,
    play_start_index,
    play_end_index,
    start_idx_used_list,
    end_idx_used_list
):

    play_poss_list = []
    for i in range(len(type_poss_list)):
        if (type_poss_list[i][0] == period_play_start and
                0 <= game_clock_play_end - type_poss_list[i][1] < time):
            play_poss_list.append([
                period_play_start,
                game_clock_play_end,
                start_region,
                end_region,
                'shot',
                shot_made_or_miss(type_poss_list[i][2].split())
            ])

            start_idx_used_list.append(play_start_index)
            # add +1 to account for play_end_index
            end_idx_used_list.append(play_end_index + 1)

    return play_poss_list, start_idx_used_list, end_idx_used_list


def get_known_player_possession(
    player_name, game_id_dict, df_pos_dist_reg_trunc,
    hometeam_id, awayteam_id, df_play_by_play, t_shot=4, t_pass=6, t_turnover=2
):
    # (assuming about 4 seconds to get to rim?)
    # (assuming 6 seconds in between pass and shot?)
    # (assuming 2 seconds between touch and turnover?)

    player_poss_idx = player_possession_idx(player_name, df_pos_dist_reg_trunc)
    player_ball_idx = player_poss_idx[2]
    next_player_ball_idx = player_poss_idx[3]

    player_team_loc = player_team_loc_from_name(player_name, game_id_dict, hometeam_id)

    df_player_impact = player_impact_df(player_name, player_team_loc, game_id_dict, df_play_by_play)

    player_game_stats = player_game_stats_nba(player_name, game_id_dict, df_player_impact)

    shoot = player_game_stats[5]
    assist = player_game_stats[0]
    turnover = player_game_stats[7]

    play_shot = []
    play_assist = []
    play_turnover = []
    start_idx_used_list = []
    end_idx_used_list = []

    for j in range(len(player_ball_idx)):
        # start of play
        play_start_index = player_ball_idx[j]
        period_play_start = df_pos_dist_reg_trunc.\
            period.values.flatten()[play_start_index]

        start_region = df_pos_dist_reg_trunc[player_name, 'region'].\
            iloc[play_start_index]

        # End of play
        play_end_index = next_player_ball_idx[j] - 1
        game_clock_play_end = df_pos_dist_reg_trunc.\
            game_clock.values.flatten()[play_end_index]

        end_region = df_pos_dist_reg_trunc[player_name, 'region'].\
            iloc[play_end_index]

        # check if possession is shot, turnover, assist:
        # shot

        for i in range(len(shoot)):
            if (shoot[i][0] == period_play_start and
                    0 <= game_clock_play_end - shoot[i][1] < t_shot):
                play_shot.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'shot',
                    shot_made_or_miss(shoot[i][2].split())
                ])

                start_idx_used_list.append(play_start_index)
                # add +1 to account for play_end_index
                end_idx_used_list.append(play_end_index + 1)

        # assist
        for i in range(len(assist)):
            if (assist[i][0] == period_play_start and
                    0 <= game_clock_play_end - assist[i][1] < t_pass):
                play_assist.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'pass',
                    'assist']
                )

                start_idx_used_list.append(play_start_index)
                end_idx_used_list.append(play_end_index + 1)

        # turnover
        for i in range(len(turnover)):
            if (turnover[i][0] == period_play_start and
                    0 <= game_clock_play_end - turnover[i][1] < t_turnover):
                play_turnover.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'turnover']
                )

                start_idx_used_list.append(play_start_index)
                end_idx_used_list.append(play_end_index + 1)

    return [
        play_shot,
        play_assist,
        play_turnover,
        start_idx_used_list,
        end_idx_used_list
    ]


def get_pass_not_assist(
    player_name,
    df_pos_dist_trunc,
    known_player_possessions,
    player_poss_idx,
    initial_shooting_side,
    hometeam_id,
    awayteam_id,
    game_id_dict,
    t=10
):
    # t= 25 corresponds to 1 sec
    # only consider a 'possession' to be when player has ball for more than t/25 seconds

    player_ball_idx = player_poss_idx[2]
    next_player_ball_idx = player_poss_idx[3]
    start_idx_used = known_player_possessions[3]
    end_idx_used = known_player_possessions[4]

    # collect possession indices

    length_possession = np.array(next_player_ball_idx) - np.array(player_ball_idx)
    no_possession = np.argwhere(length_possession < t).flatten()

    player_ball_idx = np.delete(np.array(player_ball_idx), no_possession)
    next_player_ball_idx = np.delete(np.array(next_player_ball_idx), no_possession)

    start_idx_used = np.delete(np.array(start_idx_used), no_possession)
    end_idx_used = np.delete(np.array(end_idx_used), no_possession)

    # collect the discrepancies between the nba sets and my sets, and order them

    start_idx_not_used = sorted(list(set(player_ball_idx) - set(start_idx_used)))
    end_idx_not_used = sorted(list(set(next_player_ball_idx) - set(end_idx_used)))
    play_pass = []
    player_team_id = team_id_from_name(player_name, game_id_dict)

    closest_player_to_ball = df_pos_dist_trunc['closest_player'].values.flatten()

    closest_player_team = [team_id_from_name(item, game_id_dict) for item in closest_player_to_ball]

    for i in range(len(start_idx_not_used)):
        play_start_index = start_idx_not_used[i]
        # play_end_index = end_idx_not_used[i] - 1

        # end of player possession
        end_possession_idx = end_idx_not_used[i]

        # find next time same team has ball
        # first start the list at the end index (now index =0)
        # find index of same team and add it back original index
        next_team_idx = next(closest_player_team[end_possession_idx:].index(i)
                             for i in closest_player_team[end_possession_idx:]
                             if i == player_team_id) + end_possession_idx

        # determine who the player is
        next_teammate = closest_player_to_ball[next_team_idx]

        # if next_teammate == player, just ignore it
        # either stoppage of play or something is funny

        if next_teammate != player_name:
            # check the next t indices are the same player
            # corresponding to a possession
            # if true, record it as a pass
            if len(set(closest_player_to_ball[next_team_idx:next_team_idx + t])) == 1:
                period_play_start = df_pos_dist_trunc\
                    .period.values.flatten()[play_start_index]
                # game_clock_play_start = df_pos_dist_trunc\
                #     .game_clock.values.flatten()[play_start_index]

                shooting_side = team_shooting_side(
                    player_name,
                    period_play_start,
                    initial_shooting_side,
                    hometeam_id,
                    awayteam_id
                )

                start_region = region(
                    df_pos_dist_trunc[player_name].x_loc.iloc[play_start_index],
                    df_pos_dist_trunc[player_name].y_loc.iloc[play_start_index],
                    shooting_side
                )

                # end of play
                # index where ball ends up
                game_clock_play_end = df_pos_dist_trunc\
                    .game_clock.values.flatten()[next_team_idx]

                end_region = region(
                    df_pos_dist_trunc[next_teammate].x_loc.iloc[next_team_idx],
                    df_pos_dist_trunc[next_teammate].y_loc.iloc[next_team_idx],
                    shooting_side
                )

                play_pass.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'pass']
                )
    return play_pass


def result_player_possession_df(known_player_possessions, play_pass):
    player_play_data_headers = [
        'period',
        'game_clock_end',
        'start_region',
        'end_region',
        'type'
    ]

    return pd.DataFrame(
        [known_player_possessions[0][i][:-1] for i in range(len(known_player_possessions[0]))] +
        [known_player_possessions[1][i][:-1] for i in range(len(known_player_possessions[1]))] +
        known_player_possessions[2] +
        play_pass,
        columns=player_play_data_headers
    )


def create_player_poss_dict(
    player_name,
    game_id_dict,
    df_pos_dist_trunc,
    hometeam_id,
    awayteam_id,
    initial_shooting_side,
    df_play_by_play,
    df_pos_dist_reg,
    t=10
):

    player_poss_idx = player_possession_idx(player_name, df_pos_dist_trunc)

    known_player_possessions = get_known_player_possession(
        player_name,
        game_id_dict,
        df_pos_dist_trunc,
        player_poss_idx,
        hometeam_id,
        awayteam_id,
        initial_shooting_side,
        df_play_by_play
    )

    play_pass = get_pass_not_assist(
        player_name,
        df_pos_dist_trunc,
        known_player_possessions,
        player_poss_idx,
        initial_shooting_side,
        hometeam_id,
        awayteam_id,
        t=10
    )

    df_player_possession = result_player_possession_df(known_player_possessions, play_pass)

    possession_dict = {
        'play_pass': play_pass,
        'df_player_possession': df_player_possession,
        'known_player_possessions': known_player_possessions,
        'player_poss_idx': player_poss_idx,
        'df_pos_dist_reg': df_pos_dist_reg
    }

    return possession_dict


def save_player_poss_dict(filename, possession_dict):
    with open(os.path.join(DATASETS_DIR, filename), 'wb') as json_file:
        pickle.dump(possession_dict, json_file)


# plots a visual of length of ball possessions for each team given a start
# and stop index. I don't do much with this plot


def plot_team_possession(df_pos_dist_trunc, start, stop, hometeam_id, awayteam_id, game_id_dict):

    closest_player_to_ball = df_pos_dist_trunc['closest_player'].values.flatten()

    closest_player_team = [team_id_from_name(item, game_id_dict) for item in closest_player_to_ball]

    closest_player_team = closest_player_team[start:stop]
    x_home = []
    x_away = []
    for i in range(len(closest_player_team)):
        if closest_player_team[i] == hometeam_id:
            x_home.append(i + start)
        elif closest_player_team[i] == awayteam_id:
            x_away.append(i + start)

    y_home = [0] * (len(x_home))
    y_away = [1] * (len(x_away))

    fig = plt.figure()
    ax = fig.gca()
    plt.xlim(start, stop)
    plt.ylim(0, 2)
    ax.scatter(x_home, y_home, color='blue', s=30)
    ax.scatter(x_away, y_away, color='red', s=30)
    plt.show()

    return [(x_home, y_home), (x_away, y_away)]
