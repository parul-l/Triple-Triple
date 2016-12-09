import triple_triple.player_possession_habits as pph
import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp

from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_player_possession_dataframes,
    get_df_pos_dist,
    get_df_pos_dist_trunc,
    get_df_box_score
)
from triple_triple.team_shooting_side import initial_shooting_side

df_pos_dist = get_df_pos_dist()
df_pos_dist_trunc = get_df_pos_dist_trunc()
df_pos_dist_reg = pph.get_player_court_region_df(df_pos_dist, initial_shooting_side, hometeam_id, awayteam_id)

# Get game box score from nbastats_game_data
df_box_score = get_df_box_score()


if __name__ == '__main__':

    player_name = 'Chris Bosh'
    poss_type_to_num = {
        'pass': 0,
        'shot': 1,
        'assist': 2,
        'turnover': 3
    }
    reg_to_num = {
        'back court': 0,
        'mid-range': 1,
        'key': 2,
        'out of bounds': 3,
        'paint': 4,
        'perimeter': 5
    }

    filename = 'player1_possession.json'
    possession_dict = get_player_possession_dataframes(filename)

    # returns [play_shot, play_assist, play_turnover, start_idx_used, end_idx_used]
    known_player_possessions = possession_dict['known_player_possessions']
    df_player_possession = possession_dict['df_player_possession']

    player_poss_idx = pph.player_possession_idx(player_name, df_pos_dist_trunc)

    play_pass = pph.get_pass_not_assist(
        player_name,
        df_pos_dist_trunc,
        known_player_possessions,
        player_poss_idx,
        initial_shooting_side,
        hometeam_id,
        awayteam_id,
        t=10
    )

    df_player_region = list(df_pos_dist_reg[player_name].region)
    reg_prob_dict, reg_prob_list = ppp.get_player_region_prob(player_name, df_pos_dist_reg)

    prob_poss_type = ppp.get_prob_possession_type(df_player_possession, num_outcomes=4)

    poss_per_sec = ppp.get_possession_per_second(df_box_score, player_name)

    movement_matrix = ppp.count_player_court_movement(df_player_possession)

    cond_prob_movement = ppp.cond_prob_player_court_movement(movement_matrix)

    pass_prob, shot_prob, assist_prob, turnover_prob = ppp.get_cond_prob_poss(known_player_possessions, play_pass, reg_to_num)

    player_sim_reg_temp = spp.get_player_sim_reg(reg_prob_list)
    player_sim_poss = spp.get_player_sim_poss(poss_per_sec)

    player_sim_reg, outcome_array = spp.get_simulated_play(
        player_sim_poss,
        player_sim_reg_temp,
        prob_poss_type,
        pass_prob,
        shot_prob,
        assist_prob,
        turnover_prob,
        num_outcomes=4
    )

    player_sim_coord = spp.get_simulated_coord(player_sim_reg, 'left')
