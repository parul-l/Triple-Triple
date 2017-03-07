from triple_triple.court_regions import get_region

# TODO: Fix get_df_possession_defender to limit defender's distance

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

# Also, Bosh period=2, game_clock=307 has layup on NBA stats
# but position data indicates back court and perimeter


def get_possession_df(dataframe, has_ball_dist=2.0, len_poss=25):
    # add column to characterize possession
    dataframe['action'] = None

    # filter to player-ball dist < has_ball
    df_possession_raw = dataframe\
        .query('closest_to_ball==True and dist_to_ball<=@has_ball_dist')\
        .reset_index()

    # count total number of blocks
    cond = df_possession_raw.player_id != df_possession_raw.player_id.shift()
    df_possession_raw['block'] = (cond).astype(int).cumsum()

    # groupby blocks and get length of each
    df_poss_length = df_possession_raw\
        .groupby('block')\
        .size()\
        .reset_index()
    df_poss_length.columns = ['block', 'possession_length']

    df_possession = df_possession_raw.merge(df_poss_length, on='block')

    # drop rows with length < len_poss
    df_possession = df_possession.query('possession_length >= @len_poss')

    # add possession changes
    df_possession['possession_start'] = \
        df_possession.block != df_possession.block.shift()

    df_possession['possession_end'] = \
        df_possession.block != df_possession.block.shift(-1)

    return df_possession.set_index('index')


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
    df_select_cols = df_possession[['period', 'team_id', 'x_loc', 'y_loc']]
    df_possession['region'] = df_select_cols.apply(
        lambda row: get_court_region(row, initial_shooting_side), axis=1)

    return df_possession.set_index('index')


def update_df_possession_action(end_poss_idx, action, df_possession_action):
    df_possession_action.loc[end_poss_idx, 'action'] = action


def check_action(game_clock_tuple, df_game_player, action, time_error):
    start_game_clock = game_clock_tuple[0]
    end_game_clock = game_clock_tuple[1]

    df_game_player_action_gc = df_game_player\
        .query('action==@action')\
        .game_clock.values

    if any(
            end_game_clock - time_error <= gc <= start_game_clock
            for gc in df_game_player_action_gc
    ):
        return True
    else:
        return False


def characterize_player_possessions(
    game_id,
    player_class,
    df_possession,
    df_game_stats
):
    player_id = player_class.player_id

    # query NBA's df_game_stats for specific game and player
    df_game_player = df_game_stats.query('game_id==@game_id and player_id==@player_id')

    grouped_poss_df = df_possession.groupby(['game_id', 'player_id'])

    # query on start and end of possession
    df_player_poss = grouped_poss_df\
        .get_group((game_id, player_id))\
        .query('possession_start==True or possession_end==True')

    # characterize each possession
    # index by 2 since each (start, end) is one possession

    for i in range(0, len(df_player_poss), 2):
        period = df_player_poss.period.iloc[i]
        game_clock_start = df_player_poss.game_clock.iloc[i]
        game_clock_end = df_player_poss.game_clock.iloc[i + 1]

        end_poss_idx = df_player_poss.index[i + 1]

        # check made shot
        if check_action(
            game_clock_tuple=(game_clock_start, game_clock_end),
            df_game_player=df_game_player.query('period==@period'),
            action='shot',
            time_error=5
        ):
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='shot',
                df_possession_action=df_possession
            )

        # check missed shot
        elif check_action(
            game_clock_tuple=(game_clock_start, game_clock_end),
            df_game_player=df_game_player.query('period==@period'),
            action='missed_shot',
            time_error=5
        ):
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='missed_shot',
                df_possession_action=df_possession
            )

        # check turnover
        elif check_action(
            game_clock_tuple=(game_clock_start, game_clock_end),
            df_game_player=df_game_player.query('period==@period'),
            action='turnover',
            time_error=2
        ):
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='turnover',
                df_possession_action=df_possession
            )

        # deduce pass
        else:
            update_df_possession_action(
                end_poss_idx=end_poss_idx,
                action='pass',
                df_possession_action=df_possession,
            )

    return df_possession


def get_df_possession_defender(
    players_dict,
    df_possession_region,
    df_raw_position_region,
    defender_team_id
):
    cols = [
        'period',
        'game_clock',
        'player_id',
        'player_name',
        'region',
        'x_loc',
        'y_loc'
        'dist_to_ball'
    ]

    df_other_team = df_raw_position_region.query('team_id==@defender_team_id')[cols]
    # get relevant columns and original indices before groupby
    rename_cols = [
        'period',
        'game_clock',
        'defender_id',
        'defender_name',
        'defender_region',
        'defender_x_loc',
        'defender_y_loc',
        'defender_ball_dist'
    ]

    df_other_team.columns = rename_cols

    # get closest to ball from other team
    # this takes long
    df_defender = df_other_team\
        .groupby(['period', 'game_clock'])\
        .min()\
        .reset_index()

    # merge two dataframes on period and game_clock
    for player_class in players_dict.values():
        player_id = player_class.player_id
        df_player = df_possession_region.query('player_id==@player_id')
        df_possession_defender = df_player.merge(
            df_defender,
            on=['period', 'game_clock']
        )

    return df_possession_defender
