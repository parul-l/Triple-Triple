from triple_triple.plot.full_court import draw_court_bokeh
from bokeh.io import output_file, show


def add_coord_count_col_to_action_count(row, df_coord):
    current_coord = row['has_ball_coord']
    return (df_coord.query('has_ball_coord==@current_coord')
            .coord_count.values[0])


def get_player_sim_df(df_data, player_id):
    # get df where player_action not null
    df_player_sim = df_data.query(
        'has_ball_player_id==@player_id and'
        'player_action==player_action'
    )

    # change has_ball_player_coord to strings so we can groubpy the
    # list
    df_player_sim['has_ball_player_id'] = \
        df_player_sim['has_ball_player_id'].astype(str)

    # groupby coordinates to get total actions in that region
    # kept start_play just to have a remaining column
    df_coord = df_player_sim[['has_ball_coord', 'start_play']]\
        .groupby(['has_ball_coord'])['start_play']\
        .count()\
        .reset_index(name='coord_count')

    # groupby coord and action to count action type per coord
    cols = ['has_ball_coord', 'player_action', 'start_play']
    df_action_coord = df_player_sim[cols]\
        .groupby(['has_ball_coord', 'player_action'])['start_play']\
        .count()\
        .reset_index(name='action_count')\

    df_action_coord['total_coord_count'] = \
        df_action_coord.apply(
            lambda row: add_coord_count_col_to_action_count(row, df_coord),
            axis=1
        )


    # add action/total_actions
    df_action_coord['action_to_total_action'] = \
        df_action_coord['action_count'] / df_action_coord['total_coord_count']
    
    return df_action_coord


def plot_sim_action_per_region(court_plot):
    
    
