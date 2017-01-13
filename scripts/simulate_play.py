import os
import pickle
import numpy as np

import triple_triple.simulate_player_positions as spp

from triple_triple.config import DATASETS_DIR

poss_type_to_num = {
    'pass': 0,
    'shot': 1,
    'turnover': 2
}

reg_to_num = {
    'back court': 0,
    'mid-range': 1,
    'key': 2,
    'out of bounds': 3,
    'paint': 4,
    'perimeter': 5
}

player_instances = os.path.join(DATASETS_DIR, 'player_instances.p')

with open(player_instances, 'rb') as json_file:
    player_instances = pickle.load(json_file)


if __name__ == '__main__':

    # players to be chosen to be on court
    # numbers are list_numbers in player_instances
    player_numbers = [1, 9, 10]

    players_on_court = [player_instances['player{0}'.format(item)] for item in player_numbers]

    num_sim = 40
    # outcome array keeps track of possessions:
    # [move, pass, shot_miss, shot_2pt, shot_3pt, turnover]
    outcome_array = np.zeros(6)
    player_possession_array = np.full(num_sim, np.nan)
    poss_type_array = np.full((num_sim, 2), np.nan)
    points_count = 0
    play_stop = 0
    regions = np.full(num_sim, np.nan)

    for i in range(num_sim):
        idx_ball, poss_outcome = spp.simulate_one_play(players_on_court)
        player_possession_array[i] = idx_ball
        player_with_ball = players_on_court[idx_ball]
        regions[i] = player_with_ball.court_region

        # pass
        if poss_outcome == 0:
            spp.if_pass(player_with_ball, players_on_court)
            poss_type_array[i] = [poss_outcome, -1]

            if player_with_ball.possession:
                outcome_array[0] += 1
            else:
                outcome_array[1] += 1

        # shot
        elif poss_outcome == 1:
            shot_type = spp.if_shoot(player_with_ball, players_on_court)
            play_stop += 1
            # miss
            if shot_type == 0:
                outcome_array[2] += 1
                poss_type_array[i] = [poss_outcome, 0]

            # 2 pt
            elif shot_type == 1:
                outcome_array[3] += 1
                points_count += 2
                poss_type_array[i] = [poss_outcome, 1]

            # 3 pt
            elif shot_type == 2:
                outcome_array[4] += 1
                points_count += 3
                poss_type_array[i] = [poss_outcome, 2]

        # turnover
        elif poss_outcome == 2:
            spp.if_turnover(player_with_ball, players_on_court)
            outcome_array[5] += 1
            poss_type_array[i] = [poss_outcome, -1]
            play_stop += 1
