class Player(object):
    """ Any player in the NBA at any time period.
        Attributes:
            name: A string representing the player's name
            playerid: A string representing the player's id
            teamid: A string representing player's current teamid
            jersey: A string representing player's current jersey number
            position: A string representing the player's position
            height: An integer representing player's height in inches
            weight: An integer representing player's weight in pounds

            region_prob_matrix: A 6 x 6 matrix where
                                row = start region, column = end region
                                (row, column) = probability of going from start region to end region

            action_prob_matrix: A 6 x 3 matrix where
                                row = region, column = action [0, 1, 2]
                                0 - pass, 1 - shoot, 2 - turnover

            shooting_prob: A 1 x 2 matrix where
                           0- prob of making 2 point, 1- prob of making 3pt

            region_shooting_prob: A 1 x 6 array where each entry is the
                                  prob of making a shot in the region
                                  corresponding to the entry's index

            possession_prob: Proability of having possession of the ball
                             when team is on offense (float)

            shot_attempts: An integer of the number of shots taken in a play

            shots_made: An integer of the total number of shots made

            total_points: An integer of the number of points scored

            turnovers: An integer of the total turnovers made

            passes: An integer of the total passes

            has_possession: A boolean to indicate if player has possession of ball
            
            poss_result_on_defense: An array that gives the probability of offense player's outcome when player is defending him.
            array = [0, 1, 2], where 0 - pass, 1 - shoot, 2 - turnover

            poss_result_on_defense_reg: A 6 x 3 matrix that gives defensive player's region (row) and offensive player's possession outcome (column)

            def_off_region_matrix: A 6 x 6 matrix that gives defense player (row) vs. offense player region (col)

            court_region: Int between 0 and 5
                        reg_to_num = {
                            'back court': 0,
                            'mid-range': 1,
                            'key': 2,
                            'out of bounds': 3,
                            'paint': 4,
                            'perimeter': 5
                        }
            court_coord: A tuple that reflects court region


    """

    def __init__(self, name, player_id, team_id, jersey, position, height, weight):
        self.name = name
        self.player_id = player_id
        self.team_id = team_id
        self.jersey = jersey
        self.position = position
        self.height = height
        self.weight = weight
        self.region_prob_matrix = None
        self.action_prob_matrix = None
        self.shooting_prob = None
        self.region_shooting_prob = None
        self.possession_prob = 0
        self.shot_attempts = 0
        self.shots_made = 0
        self.total_points = 0
        self.turnovers = 0
        self.passes = 0
        self.has_possession = False
        self.poss_result_on_defense = None
        self.poss_result_on_defense_reg = None
        self.court_region = None
        self.court_coord = None


def playerid_from_name(player_name, game_player_dict):
    for playerid, player_info in game_player_dict.items():
        if player_info[0] == player_name:
            return playerid


def create_player_class_instance(
    player_list,
    game_player_dict,
    df_player_bio=None
):
    player_class_dict = {}
    for player_id in player_list:
        info_list = game_player_dict[str(player_id)]

        name = info_list[0]
        team_id = int(info_list[2])
        jersey = info_list[1]
        position = info_list[3]

        if df_player_bio is None:
            height = 0
            weight = 0
        else:
            height = df_player_bio\
                .query('player_id==@player_id')\
                .height.iloc[0]
            weight = df_player_bio\
                .query('player_id==@player_id')\
                .weight.iloc[0]

        player_class_dict[player_id] = \
            Player(
                name=name,
                player_id=player_id,
                team_id=team_id,
                jersey=jersey,
                position=position,
                height=height,
                weight=weight
            )

    return player_class_dict


def player_class_reset(player_class_dict):
    for player_class in player_class_dict.values():
        player_class.shot_attempts = 0
        player_class.shots_made = 0
        player_class.total_points = 0
        player_class.turnovers = 0
        player_class.passes = 0
        player_class.has_possession = False
        player_class.court_region = None
        player_class.court_coord = None
