import os
import pickle

import triple_triple.prob_player_possessions as ppp

from triple_triple.config import DATASETS_DIR
from triple_triple.startup_data import (
    get_game_id_dict,
    get_player_possession_dataframes,
    get_df_box_score
)

game_id_dict = get_game_id_dict()
# Get game box score from nbastats_game_data
df_box_score = get_df_box_score()

"""
    This file uses the results of run_player_possession_habits, which outputs 'player_i_poss_dfs.json' for each player i in player list. Each json file contains known_player_possessions and df_player_possession.

    After current script is run, delete each 'player_i_poss_dfs.json' because this info is contained in pickeled_file.
"""


if __name__ == '__main__':

    pickeled_file = os.path.join(DATASETS_DIR, 'player_instances_info.p')

    if os.path.exists(pickeled_file):
        with open(pickeled_file, 'rb') as a_file:
            data = pickle.load(a_file)

        player_list = data['player_list']
        simulated_regions_dict = data['simulated_regions_dict']
        all_players_poss_prob_dict = data['all_players_poss_prob_dict']
        all_players_outcome_prob_matrix_dict = data['all_players_outcome_prob_matrix_dict']

    else:
        # same order as run_player_possession habits
        # to keep order of the poss_df.json 's

        player_list = [value[0] for value in game_id_dict.values()]

        player_list.remove('ball')

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
                df_pos_dist_reg,
                player_name,
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

            reg_prob_list_no_bc = ppp.get_reg_prob_no_backcourt(reg_prob_list)

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
                reg_prob_list_no_bc,
                reg_prob_list,
                prob_poss_type,
                prob_shot_type,
                prob_assist,
                poss_per_sec
            ]
    data = {
        'player_list': player_list,
        'all_players_poss_prob_dict': all_players_poss_prob_dict,
        'all_players_outcome_prob_matrix_dict': all_players_outcome_prob_matrix_dict,
    }

    with open(pickeled_file, 'wb') as a_file:
        pickle.dump(data, a_file)
