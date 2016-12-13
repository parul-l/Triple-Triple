import numpy as np

import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp


from triple_triple.startup_data import (
    get_player_possession_dataframes,
    get_df_box_score
)


if __name__ == '__main__':

    # Get game box score from nbastats_game_data
    df_box_score = get_df_box_score()

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
    play_pass = possession_dict['play_pass']
    player_poss_idx = possession_dict['player_poss_idx']
    df_pos_dist_reg = possession_dict['df_pos_dist_reg']

    df_player_region = list(df_pos_dist_reg[player_name].region)

    # use reg_to_num: 0 position = back court, etc
    reg_prob_dict, reg_prob_list = ppp.get_player_region_prob(player_name, df_pos_dist_reg)

    # return [prob_pass, prob_shot, prob_assist, prob_turnover]
    prob_poss_type = ppp.get_prob_possession_type(df_player_possession, num_outcomes=4)

    prob_shot_type = ppp.get_shot_type_prob(known_player_possessions)

    poss_per_sec = ppp.get_possession_per_second(df_box_score, player_name)

    # use reg_to_num
    # (0,2) position means possession started at backcourt and ended at key
    movement_matrix = ppp.count_player_court_movement(df_player_possession)
    # prob of going from back court to key is (0, 2) entry
    cond_prob_movement = ppp.cond_prob_player_per_region(movement_matrix)

    # shot per region count
    miss_shots_matrix = ppp.get_player_scoring_prob_region(known_player_possessions, 0)
    _2pt_shots_matrix = ppp.get_player_scoring_prob_region(known_player_possessions, 2)
    _3pt_shots_matrix = ppp.get_player_scoring_prob_region(known_player_possessions, 3)

    # shot per region_probabilities
    miss_shots_prob_matrix = ppp.cond_prob_player_per_region(miss_shots_matrix)
    _2pt_shots_prob_matrix = ppp.cond_prob_player_per_region(_2pt_shots_matrix)
    _3pt_shots_prob_matrix = ppp.cond_prob_player_per_region(_3pt_shots_matrix)

    # matrices of conditional probabilities
    # (0, 2) in pass_prob gives prob of passing from backcourt to key
    pass_prob_matrix, shot_prob_matrix, assist_prob_matrix, turnover_prob_matrix = ppp.get_cond_prob_poss(
        known_player_possessions, play_pass, reg_to_num)

    # simulate where a player is when he is on the court
    player_sim_reg_temp = spp.get_player_sim_reg(reg_prob_list, num_sim=5000)

    # of all the moments on the court, simulate when he has posssesssion
    # 0 = no possession, 1 = possession
    player_sim_poss = spp.get_player_sim_poss(poss_per_sec, num_sim=5000)

    # outcome array keeps track of possessions:
    # [pass, shot_miss, shot_2pt, shot_3pt, assist, turnover]
    # points increase by 2 for every assist
    player_sim_reg, outcome_array, points = spp.get_simulated_play(
        player_sim_poss,
        player_sim_reg_temp,
        prob_poss_type,
        prob_shot_type,
        pass_prob_matrix,
        assist_prob_matrix,
        turnover_prob_matrix,
        miss_shots_prob_matrix,
        _2pt_shots_prob_matrix,
        _3pt_shots_prob_matrix,
        num_outcomes=4
    )

    player_sim_coord = spp.get_simulated_coord(player_sim_reg, 'left')
