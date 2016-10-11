import numpy as np
import pandas as pd

from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_pos_dist,
    get_df_play_by_play,
)

game_id_dict = get_game_id_dict()
df_pos_dist = get_df_pos_dist()
df_play_by_play = get_df_play_by_play()

def open_json(file_name):
    json_data = open(file_name).read()
    return json.loads(json_data)

def team_id_from_name(player_name):
    for player_info in game_id_dict.values():
        if player_info[0] == player_name:
            return player_info[2]

# find index of first score
def get_initial_shooting_sides(df_play_by_play, df_pos_dist,
    hometeam_id, awayteam_id, has_ball_dist=2):

    df_pos_dist_trunc = df_pos_dist[(df_pos_dist.min_dist < has_ball_dist)\
                            .any(axis=1)].reset_index()

    # determine first score
    score = list(df_play_by_play.SCORE.values)
    first_score_idx = next(score.index(item) for item in score if type(item) == str)

    # find time, player
    first_score_period = df_play_by_play.PERIOD.iloc[first_score_idx]
    first_score_game_clock = df_play_by_play.PCTIMESTRING.iloc[first_score_idx]
    first_score_player = df_play_by_play.PLAYER1_NAME.iloc[first_score_idx]
    first_score_team = team_id_from_name(first_score_player)

    # assuming it takes 4 seconds for ball to reach rim
    first_score = df_pos_dist_trunc[
        (df_pos_dist_trunc.closest_player.values.flatten() == first_score_player) &
        (df_pos_dist_trunc.period.values.flatten() == first_score_period) &
        (df_pos_dist_trunc.game_clock.values.flatten() >= first_score_game_clock) &
        (df_pos_dist_trunc.game_clock.values.flatten() <= first_score_game_clock + 4)
    ]

    first_score_xcoord = first_score[first_score_player].x_loc.iloc[0]
    if  ((first_score_xcoord <= 47 and first_score_team == hometeam_id) or
        (first_score_xcoord > 47 and first_score_team == awayteam_id)):
        return {hometeam_id: 'left', awayteam_id: 'right'}
    elif ((first_score_xcoord <= 47 and first_score_team == awayteam_id) or
        (first_score_xcoord > 47 and first_score_team == hometeam_id)):
        return {awayteam_id: 'left', hometeam_id: 'right'}

def team_shooting_side(player, period, initial_shooting_side, hometeam_id, awayteam_id):
    team = team_id_from_name(player)
    if team == hometeam_id:
        if (period == 1 or period == 2):
            return initial_shooting_side[team]
        elif (period == 3 or period == 4):
            return initial_shooting_side[awayteam_id]
    elif team == awayteam_id:
        if (period == 1 or period == 2):
            return initial_shooting_side[team]
        elif (period == 3 or period == 4):
            return initial_shooting_side[hometeam_id]

initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_pos_dist,
                            hometeam_id, awayteam_id, has_ball_dist=2)

##############################
##############################

if __name__=='__main__':
    player = 'Chris Bosh'
    period = 1
    initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_pos_dist,
                                hometeam_id, awayteam_id, has_ball_dist=2)

    shooting_side = team_shooting_side(player, period, initial_shooting_side,
                        hometeam_id, awayteam_id)
