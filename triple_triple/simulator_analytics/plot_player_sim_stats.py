
def add_coord_count_col_to_action_count(row, df_coord):
    current_coord_x = row['has_ball_coord_x']
    current_coord_y = row['has_ball_coord_y']
    coord_query = ('has_ball_coord_x==@current_coord_x and '
                   'has_ball_coord_y==@current_coord_y')
    return df_coord.query(coord_query).coord_count.values[0]


def get_player_sim_df(df_data, player_id):
    # get df where player_action not null
    df_player_sim = df_data.query(
        'has_ball_player_id==@player_id and '
        'player_action==player_action'
    )

    # change has_ball_player_coord to strings so we can groubpy the
    # list

    # groupby coordinates to get total actions in that region
    # kept start_play just to have a remaining column
    rel_col1 = [
        'has_ball_coord_x',
        'has_ball_coord_y',
        'start_play'
    ]
    df_coord = df_player_sim[rel_col1]\
        .groupby(rel_col1[:-1])['start_play']\
        .count()\
        .reset_index(name='coord_count')

    # groupby coord and action to count action type per coord
    rel_col2 = [
        'has_ball_coord_x',
        'has_ball_coord_y',
        'player_action',
        'start_play'
    ]
    df_action_coord = df_player_sim[rel_col2]\
        .groupby(rel_col2[:-1])\
        ['start_play']\
        .count()\
        .reset_index(name='action_count')

    df_action_coord['total_coord_count'] = \
        df_action_coord.apply(
            lambda row: add_coord_count_col_to_action_count(row, df_coord),
            axis=1
        )


    # add action/total_actions
    df_action_coord['action_to_total_action'] = \
        df_action_coord['action_count'] / df_action_coord['total_coord_count']
    
    return df_action_coord
