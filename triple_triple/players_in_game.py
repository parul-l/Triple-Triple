from triple_triple.data_generators.nbastats_game_data import box_score_df

# game_info_dict is specifically for gameid = '0021500568', but params_box_score has game_id as input

# METHOD 1
# Use df_raw_position
def get_players_in_game(df_raw_position, team_id):
    return df_raw_position\
        .query('team_id==@team_id')\
        .player_id\
        .unique()

# METHOD 2
# Use df_box_score
# def get_players_in_game(
#     base_url_box_score,
#     params_box_score,
#     game_info_dict
# ):
#
#     df_box_score = box_score_df(base_url_box_score, params_box_score)
#
#     hometeam_id = game_info_dict['hometeam_id']
#     visitorteam_id = game_info_dict['visitorteam_id']
#
#     # player_id_lists
#     home_player_id_list = df_box_score\
#         .query('TEAM_ID==@hometeam_id and MIN!=0')\
#         .PLAYER_ID\
#         .values
#
#     visitor_player_id_list = df_box_score\
#         .query('TEAM_ID==@visitorteam_id and MIN!=0')\
#         .PLAYER_ID\
#         .values
#
#     return home_player_id_list, visitor_player_id_list
