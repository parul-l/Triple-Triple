import numpy as np
from triple_triple.court_regions import get_region

# TODO: Fix get_possession_df. Right now it is double counting possessions. Perhaps check ball height/moment? Here Wade has the ball as two separate possessions
# 867984       4      114.74     Dwyane Wade
# 867995       4      114.70     Dwyane Wade
# 868006       4      114.66     Dwyane Wade
# 868017       4      114.62     Dwyane Wade
# 868028       4      114.58     Dwyane Wade
# 868039       4      114.54     Dwyane Wade
# 868047       4      114.50   Klay Thompson
# 868058       4      114.46   Klay Thompson
# 868069       4      114.42   Klay Thompson
# 868080       4      114.38   Klay Thompson
# 868094       4      114.34     Dwyane Wade
# 868105       4      114.30     Dwyane Wade
# 868116       4      114.26     Dwyane Wade
# 868127       4      114.23     Dwyane Wade
# 868138       4      114.19     Dwyane Wade
# 868149       4      114.15     Dwyane Wade
# 868160       4      114.11     Dwyane Wade
# 868171       4      114.07     Dwyane Wade


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
        df_possession.loc[idx_poss_change[idx] + 1, 'possession'] = 'Start'
        df_possession.loc[idx_poss_change[idx + 1], 'possession'] = 'Stop'

        df_possession.loc[idx_poss_change[idx] + 2:idx_poss_change[idx + 1] - 1, 'possession'] = True

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


def add_regions_to_df(df_possession, initial_shooting_side):
    df_select = df_possession[['period', 'team_id', 'x_loc', 'y_loc']]
    regions_array = df_select.apply(lambda row: get_court_region(row, initial_shooting_side), axis=1)
    df_possession['region'] = regions_array

    return df_possession


def add_empty_action_to_df_raw(df_possession):
    df_possession['action'] = None

    return df_possession


def update_df_possession_action(end_poss_idx, action, df_possession_action):
    df_possession_action.loc[end_poss_idx, 'action'] = action


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


def characterize_possession_one_game_player(game_id, player_id, df_possession_action, df_game_stats):

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
            time_error=5
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
            action='turnover',
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


def get_multi_games_players_possessions(game_id_list, player_id_list, df_possession_action, df_game_stats):
    # query on game_id and player_id to get truncated dataframe
    df_possession_action = df_possession_action[
        df_possession_action.game_id.isin(game_id_list) & df_possession_action.player_id.isin(player_id_list)
    ]

    for game in game_id_list:
        game_id = game
        df_game_stats = df_game_stats.query('game_id==@game_id')
        for player in player_id_list:
            player_id = player
            df_possession_action = characterize_possession_one_game_player(
                game_id=game_id,
                player_id=player_id,
                df_possession_action=df_possession_action,
                df_game_stats=df_game_stats
            )

    return df_possession_action
