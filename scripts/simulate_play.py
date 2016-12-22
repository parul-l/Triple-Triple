import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp

from triple_triple.startup_data import (
    get_player_possession_dataframes,
    get_df_box_score
)

# Get game box score from nbastats_game_data
df_box_score = get_df_box_score()

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


if __name__ == '__main__':
    player_list = [
        'Chris Bosh',
        # 'Luol Deng',
        # 'Dwyane Wade'
    ]

    num_players = len(player_list)

    # collect probabilities
    all_players_poss_prob_dict = {}
    all_players_outcome_prob_matrix_dict = {}

    for i in range(num_players):
        player_name = player_list[i]
        player_number = str(i)
        filename = 'player' + player_number + 'poss_dfs.json'

        possession_dict = get_player_possession_dataframes(filename)

        # get all items/values from possession_dict
        # known_player_possessions returns:
        # [play_shot, play_assist, play_turnover, start_idx_used, end_idx_used]
        known_player_possessions = possession_dict['known_player_possessions']
        df_player_possession = possession_dict['df_player_possession']
        play_pass = possession_dict['play_pass']
        player_poss_idx = possession_dict['player_poss_idx']
        df_pos_dist_reg = possession_dict['df_pos_dist_reg']

        # get list of outcome prob matrices
        player_outcome_prob_matrix_list = ppp.get_player_outcome_prob_matrix_list(
            df_player_possession,
            known_player_possessions,
            play_pass,
            reg_to_num
        )
        # add player_outcome prob matrices to dict
        # list order:
        # 0 movement_prob_matrix,
        # 1 miss_shots_prob_matrix,
        # 2 _2pt_shots_prob_matrix,
        # 3 _3pt_shots_prob_matrix,
        # 4 pass_prob_matrix,
        # 5 shot_prob_matrix,
        # 6 assist_prob_matrix,
        # 7 turnover_prob_matrix

        all_players_outcome_prob_matrix_dict[player_name] = player_outcome_prob_matrix_list

        reg_prob_dict, reg_prob_list = ppp.get_player_region_prob(player_name, df_pos_dist_reg)
        # return [prob_pass, prob_shot, prob_turnover]
        prob_poss_type = ppp.get_prob_possession_type(df_player_possession, num_outcomes=3)

        # returns [miss, 2pt, 3pt]
        prob_shot_type = ppp.get_shot_type_prob(known_player_possessions)

        # prob assist
        prob_assist = ppp.get_assist_prob(known_player_possessions, df_player_possession)

        # returns possession per second
        poss_per_sec = ppp.get_possession_per_second(df_box_score, player_name)

        # add reg_prob_list to dict
        all_players_poss_prob_dict[player_name] = [
            reg_prob_list,
            prob_poss_type,
            prob_shot_type,
            prob_assist,
            poss_per_sec
        ]

    ############################
    # MULTIPLE PLAYER SIMULATION
    ############################
    # simulate regions, coordinates and play
    for i in range(num_players):
        # regions and coordinates
        simulated_regions_dict = spp.get_simulated_regions_dict(player_list, all_players_poss_prob_dict, all_players_outcome_prob_matrix_dict)
        simulated_region_coord_dict = spp.get_simulated_region_coord_dict(player_list, simulated_regions_dict)

    # simulate play
    outcome_array, player_possession_array, points_count = spp.get_simulate_play_mult_players(
        player_list,
        simulated_regions_dict,
        simulated_region_coord_dict,
        all_players_poss_prob_dict,
        all_players_outcome_prob_matrix_dict
    )

    ############################
    # ONE PLAYER SIMULATION
    ############################
    # simulate region where a player is when he is on the court
    player_sim_reg_temp = spp.get_player_sim_reg(
        reg_prob_list,
        all_players_outcome_prob_matrix_dict[player_list[0]][0],
        num_sim=5000,
        num_regions=6
    )

    # of all the moments on the court, simulate when he has posssesssion
    # 0 = no possession, 1 = possession
    player_sim_poss = spp.get_player_sim_poss(poss_per_sec, num_sim=len(player_sim_reg_temp))

    # outcome array keeps track of possessions:
    # [pass, shot_miss, shot_2pt, shot_3pt, assist, turnover]
    # points increase by 2 for every assist
    player_sim_reg, outcome_array, points = spp.get_simulated_play(
        player_sim_poss,
        player_sim_reg_temp,
        prob_poss_type,
        prob_shot_type,
        prob_assist,
        all_players_outcome_prob_matrix_dict[player_list[0]][4],
        all_players_outcome_prob_matrix_dict[player_list[0]][6],
        all_players_outcome_prob_matrix_dict[player_list[0]][7],
        all_players_outcome_prob_matrix_dict[player_list[0]][1],
        all_players_outcome_prob_matrix_dict[player_list[0]][2],
        all_players_outcome_prob_matrix_dict[player_list[0]][3],
        num_outcomes=4
    )

    player_sim_coord = spp.get_simulated_coord(player_sim_reg, 'left')
