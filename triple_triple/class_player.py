import numpy as np

class Player(object):
    """ Any player in the NBA at any time period.
        Attributes:
            name: A string representing the player's name
            playerid: A string representing the player's id
            teamid: A string representing player's current teamid
            prob_lists: A list of lists of probabilities
                        [reg_prob_list_no_bc,
                        reg_prob_list,
                        prob_poss_type, ([prob_pass, prob_shot, prob_turnover])
                        prob_shot_type, ([miss, 2pt, 3pt])
                        prob_assist,
                        poss_per_sec]

            prob_matrices: A list of conditional probabilities (positions, passes, shots, turnovers)
                    [
                    0-movement_prob_matrix,
                    1-miss_shots_prob_matrix,
                    2-_2pt_shots_prob_matrix,
                    3-_3pt_shots_prob_matrix,
                    4-pass_prob_matrix,
                    5-shot_prob_matrix,
                    6-assist_prob_matrix,
                    7-turnover_prob_matrix]

            possession: A boolean to indicate if player has possession of ball

            court_region: Int between 0 and 5
                        reg_to_num = {
                            'back court': 0,
                            'mid-range': 1,
                            'key': 2,
                            'out of bounds': 3,
                            'paint': 4,
                            'perimeter': 5
                        }


    """

    def __init__(self, name, playerid, teamid, prob_lists, prob_matrices):
        self.name = name
        self.playerid = playerid
        self.teamid = teamid
        self.prob_lists = prob_lists
        self.prob_matrices = prob_matrices
        self.possession = False
        self.court_region = 0


def playerid_from_name(player_name, game_id_dict):
    for playerid, player_info in game_id_dict.items():
        if player_info[0] == player_name:
            return playerid
