class Player(object):
    """ Any player in the NBA at any time period.
        Attributes:
            name: A string representing the player's name
            playerid: A string representing the player's id
            teamid: A string representing player's current teamid
            prob_lists: A list of lists of probabilities
                    [
                    0 - reg_prob_list,
                    1 - ]

            prob_matrices: A list of conditional probabilities (positions, passes, shots, turnovers)
                    [
                    0 - movement_prob_matrix,
                    1 - ]

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

    def __init__(self, name, player_id, team_id):
        self.name = name
        self.player_id = player_id
        self.team_id = team_id
        self.prob_lists = None
        self.prob_matrices = None
        self.possession = False
        self.court_region = 0


def playerid_from_name(player_name, game_player_dict):
    for playerid, player_info in game_player_dict.items():
        if player_info[0] == player_name:
            return playerid


def create_player_class_instance(player_list, game_player_dict):
    player_class_dict = {}
    for player_id in player_list:
        player_class_dict['_' + str(player_id)] = \
            Player(
                name=game_player_dict[str(player_id)][0],           # name
                player_id=player_id,                                # player_id
                team_id=int(game_player_dict[str(player_id)][2]),   # team_id
        )

    return player_class_dict
