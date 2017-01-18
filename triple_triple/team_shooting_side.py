from triple_triple.startup_data import (
    get_df_raw_position_data,
    get_game_info_dict,
    get_game_player_dict,
    get_df_play_by_play
)

game_info_dict = get_game_info_dict()
game_player_dict = get_game_player_dict()
df_play_by_play = get_df_play_by_play()
df_raw_position_data = get_df_raw_position_data()

def get_initial_shooting_sides(df_play_by_play, df_raw_position_data, game_info_dict):

    # hometeam_id/visitorteam_id
    hometeam_id = game_info_dict['hometeam_id']
    awayteam_id = game_info_dict['visitorteam_id']

    # determine first score
    score = list(df_play_by_play.SCORE.values)
    first_score_idx = next(score.index(item) for item in score if type(item) == str)

    # find time of first shot
    first_score_period = df_play_by_play.PERIOD.iloc[first_score_idx]
    first_score_game_clock = df_play_by_play.PCTIMESTRING.iloc[first_score_idx]
    first_score_team = df_play_by_play.PLAYER1_TEAM_ID.iloc[first_score_idx]

    # find location of ball at time assuming +/- 0.2 clock difference
    df_first_shot = df_raw_position_data.query(
        'period == @first_score_period and '
        'player_id == -1 and '
        '@first_score_game_clock - 0.2 < game_clock < @first_score_game_clock + 0.2')[['x_loc', 'y_loc']].tail(1)

    x_coord = df_first_shot.x_loc.values[0]

    if ((x_coord <= 47 and first_score_team == hometeam_id) or
            (x_coord > 47 and first_score_team == awayteam_id)):
        return {hometeam_id: 'left', awayteam_id: 'right'}
    else:
        return {awayteam_id: 'left', hometeam_id: 'right'}
