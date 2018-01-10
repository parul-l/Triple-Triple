import numpy as np
import pandas as pd


def get_initial_shooting_sides(
    df_games,
    df_play_by_play,
    df_game_positions
):
    # hometeam_id/visitorteam_id
    home_team_id = df_games['home_team_id'].iloc[0]
    visitor_team_id = df_games['visitor_team_id'].iloc[0]

    # first score (index where score diff not null)
    first_score_idx = np.where(
        pd.notnull(df_play_by_play.score_diff))[0][0]

    # find time of first shot
    first_score_period = df_play_by_play.period.iloc[first_score_idx]
    first_score_game_clock = df_play_by_play.pctimestring.iloc[first_score_idx]
    first_score_team = df_play_by_play.player1_team_id.iloc[first_score_idx]

    # find x-coord of ball at time assuming +/- 0.2 clock difference
    query_params = (
        'period == @first_score_period and '
        'player_id == -1 and '
        'abs(@first_score_game_clock - period_clock) < 0.2'
    )

    x_coord = df_game_positions\
        .query(query_params)\
        .tail(1)\
        .x_coordinate.values[0]

    if ((x_coord <= 47 and first_score_team == home_team_id) or
            (x_coord > 47 and first_score_team == visitor_team_id)):
        return {home_team_id: 'left', visitor_team_id: 'right'}
    else:
        return {visitor_team_id: 'left', home_team_id: 'right'}


# from triple_triple.startup_data import (
#     get_df_raw_position_data,
#     get_game_info_dict,
#     get_game_player_dict,
#     get_df_play_by_play
# )

# game_info_dict = get_game_info_dict()
# game_player_dict = get_game_player_dict()
# df_play_by_play = get_df_play_by_play()
# df_raw_position_data = get_df_raw_position_data()


# def get_initial_shooting_sides(
#     df_play_by_play,
#     df_raw_position_data,
#     game_info_dict
# ):

#     # hometeam_id/visitorteam_id
#     hometeam_id = game_info_dict['hometeam_id']
#     awayteam_id = game_info_dict['visitorteam_id']

#     # determine first score
#     score = list(df_play_by_play.SCORE.values)
#     first_score_idx = next(
#         score.index(item) for item in score if type(item) == str
#     )

#     # find time of first shot
#     first_score_period = df_play_by_play.PERIOD.iloc[first_score_idx]
#     first_score_game_clock = df_play_by_play.PCTIMESTRING.iloc[first_score_idx]
#     first_score_team = df_play_by_play.PLAYER1_TEAM_ID.iloc[first_score_idx]

#     # find x-coord of ball at time assuming +/- 0.2 clock difference
#     query_params = (
#         'period == @first_score_period and '
#         'player_id == -1 and '
#         'abs(@first_score_game_clock - game_clock) < 0.2'
#     )

#     x_coord = df_raw_position_data\
#         .query(query_params)\
#         .tail(1)\
#         .x_loc.values[0]

#     if ((x_coord <= 47 and first_score_team == hometeam_id) or
#             (x_coord > 47 and first_score_team == awayteam_id)):
#         return {hometeam_id: 'left', awayteam_id: 'right'}
#     else:
#         return {awayteam_id: 'left', hometeam_id: 'right'}
