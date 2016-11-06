import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from triple_triple.court_regions import region
from triple_triple.data_generators.player_game_stats_data import (
    player_impact_df,
    player_game_stats_nba
)
from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_pos_dist,
    get_df_pos_dist_trunc,
    get_df_play_by_play,
)
from triple_triple.team_shooting_side import (
    team_id_from_name,
    initial_shooting_side,
    team_shooting_side
)

# player_court_region determines player's region every moment he is on the court
# and hence uses df_pos_dist

# player possession functions use df_pos_dist_trunc, which considers
# players closest to ball when dist < 2

game_id_dict = get_game_id_dict()
df_pos_dist = get_df_pos_dist()
df_pos_dist_trunc = get_df_pos_dist_trunc()
df_play_by_play = get_df_play_by_play()


# has_ball_dist dist set to same dist used in get_df_pos_dist_trunc
def get_pos_trunc_df(df_pos, has_ball_dist=2):
    return df_pos[df_pos['min_dist'].values < has_ball_dist].reset_index()


def get_player_court_region_df(df_pos_dist):
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


def player_possession_idx(player, df_pos_dist_trunc):
    closest_player_to_ball = df_pos_dist_trunc.closest_player.values.flatten()

    player_ball = [None] * len(closest_player_to_ball)
    next_player_ball = [None] * len(closest_player_to_ball)

    player_ball_idx = []
    next_player_ball_idx = []

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


def characterize_player_possessions(player_name, df_pos_dist_trunc,
                                    player_poss_idx, hometeam_id, awayteam_id,
                                    initial_shooting_side, df_play_by_play):

    player_ball_idx = player_poss_idx[2]
    next_player_ball_idx = player_poss_idx[3]

    df_player_impact = player_impact_df(player_name, hometeam_id, df_play_by_play)
    player_game_stats = player_game_stats_nba(player_name, df_player_impact)

    shoot = player_game_stats[5]
    assist = player_game_stats[0]
    turnover = player_game_stats[7]

    play_shot = []
    play_assist = []
    play_turnover = []
    start_idx_used = []
    end_idx_used = []

    for j in range(len(player_ball_idx)):
        # start of play
        play_start_index = player_ball_idx[j]
        period_play_start = df_pos_dist_trunc.\
            period.values.flatten()[play_start_index]
        # game_clock_play_start = df_pos_dist_trunc.\
        #     game_clock.values.flatten()[play_start_index]

        shooting_side = team_shooting_side(
            player_name, period_play_start,
            initial_shooting_side,
            hometeam_id,
            awayteam_id
        )

        start_region = region(
            df_pos_dist_trunc[player_name].x_loc.iloc[play_start_index],
            df_pos_dist_trunc[player_name].y_loc.iloc[play_start_index],
            shooting_side
        )

        # End of play
        play_end_index = next_player_ball_idx[j] - 1
        game_clock_play_end = df_pos_dist_trunc.\
            game_clock.values.flatten()[play_end_index]

        end_region = region(
            df_pos_dist_trunc[player_name].x_loc.iloc[play_end_index],
            df_pos_dist_trunc[player_name].y_loc.iloc[play_end_index],
            shooting_side
        )

        # check if possession is shot, turnover, assist:

        # shot (assuming about 4 seconds to get to rim?)
        for i in range(len(shoot)):
            if (shoot[i][0] == period_play_start and
                    0 <= game_clock_play_end - shoot[i][1] < 4):
                play_shot.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'shot']
                )

                start_idx_used.append(play_start_index)
                # add +1 to account for play_end_index
                end_idx_used.append(play_end_index + 1)

        # assist (assuming 6 seconds in between pass and shot)
        for i in range(len(assist)):
            if (assist[i][0] == period_play_start and
                    0 <= game_clock_play_end - assist[i][1] < 6):
                play_assist.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'assist']
                )

                start_idx_used.append(play_start_index)
                end_idx_used.append(play_end_index + 1)

        # turnover (assuming 2 seconds between touch and turnover)
        for i in range(len(turnover)):
            if (turnover[i][0] == period_play_start and
                    0 <= game_clock_play_end - turnover[i][1] < 2):
                play_turnover.append([
                    period_play_start,
                    game_clock_play_end,
                    start_region,
                    end_region,
                    'turnover']
                )

                start_idx_used.append(play_start_index)
                end_idx_used.append(play_end_index + 1)

    return [
        play_shot,
        play_assist,
        play_turnover,
        start_idx_used,
        end_idx_used
    ]

# t= 25 corresponds to 1 sec
# only consider a 'possession' to be when player has ball for more than t seconds


def get_pass_not_assist(
    player_name,
    df_pos_dist_trunc,
    known_player_possessions,
    player_poss_idx,
    t=10
):

    player_ball_idx = player_poss_idx[2]
    next_player_ball_idx = player_poss_idx[3]
    start_idx_used = known_player_possessions[3]
    end_idx_used = known_player_possessions[4]

    # collect possession indices

    length_possession = np.array(next_player_ball_idx) - np.array(player_ball_idx)
    possession = np.argwhere(length_possession < t).flatten()

    player_ball_idx = np.delete(np.array(player_ball_idx), possession)
    next_player_ball_idx = np.delete(np.array(next_player_ball_idx), possession)

    start_idx_used = np.delete(np.array(start_idx_used), possession)
    end_idx_used = np.delete(np.array(end_idx_used), possession)

    # collect the discrepancies between the nba sets and my sets, and order them

    start_idx_not_used = sorted(list(set(player_ball_idx) - set(start_idx_used)))
    end_idx_not_used = sorted(list(set(next_player_ball_idx) - set(end_idx_used)))
    play_pass = []
    player_team_id = team_id_from_name(player_name)

    closest_player_to_ball = df_pos_dist_trunc['closest_player'].values.flatten()

    closest_player_team = [team_id_from_name(item) for item in closest_player_to_ball]

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

        # if next_teammate ==player, just ignore it
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
                    df_pos_dist_trunc[player].y_loc.iloc[play_start_index],
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
        known_player_possessions[0] +
        known_player_possessions[1] +
        known_player_possessions[2] +
        play_pass,
        columns=player_play_data_headers
    )

# plots a visual of length of ball possessions for each team given a start
# and stop index. I don't do much with this plot


def plot_team_possession(start, stop, hometeam_id, awayteam_id):

    closest_player_to_ball = df_pos_dist_trunc['closest_player'].values.flatten()

    closest_player_team = [team_id_from_name(item) for item in closest_player_to_ball]

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


##################################
##################################
if __name__ == '__main__':

    reg_to_num = {
        'back court': 0,
        'mid-range': 1,
        'key': 2,
        'out of bounds': 3,
        'paint': 4,
        'perimeter': 5
    }

    player = 'Chris Bosh'
    df_pos_dist_reg = get_player_court_region_df(df_pos_dist)
    df_pos_dist_reg_trunc = get_pos_trunc_df(df_pos_dist_reg)
    player_poss_idx = player_possession_idx(player, df_pos_dist_trunc)

    # returns [play_shot, play_assist, play_turnover, start_idx_used, end_idx_used]
    known_player_possessions = characterize_player_possessions(
        player,
        df_pos_dist_trunc,
        player_poss_idx,
        hometeam_id,
        awayteam_id,
        initial_shooting_side,
        df_play_by_play
    )

    play_pass = get_pass_not_assist(
        player,
        df_pos_dist_trunc,
        known_player_possessions,
        player_poss_idx,
        t=10
    )

    df_player_possession = result_player_possession_df(known_player_possessions, play_pass)

    # plot_coord = plot_team_possession(10, 20, hometeam_id, awayteam_id)
