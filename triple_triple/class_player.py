class Player(object):
    """ Any player in the NBA at any time period.
        Attributes:
            name: A string representing the player's name
                playerid: An int representing the player's id
            teamid: A string representing player's current teamid
                jersey: A string representing player's current jersey number
            position: A string representing the player's position
            height: An integer representing player's height in
                inches
            weight: An integer representing player's weight in
                pounds


            region_freq_matrix: A 6 x 6 matrix where
                row = start region, column = end region
                (row, column) = frequency count of going from start region to end region

            region_prob_matrix: A 6 x 6 matrix where
                row = start region, column = end region
                (row, column) = probability of going from start region to end region

            action_freq_matrix: A 6 x 3 matrix where
                row = region, column = action [0, 1, 2]
                0 - pass, 1 - shoot, 2 - turnover
                (row, column) = frequency count of action per region

            action_prob_matrix: A 6 x 3 matrix where
                row = region, column = action [0, 1, 2]
                0 - pass, 1 - shoot, 2 - turnover
                (row, column) = probability of action per region

            shooting_freq: A 1 x 2 matrix where each element is a tuple:
                0- (freq of making 2 point, total 2 point attempts)
                1- (freq of making 3 point, total 3 point attempts)

            shooting_prob: A 1 x 2 matrix where
                0- prob of making 2 point, 1- prob of making 3pt

            region_shooting_freq: A dictionary with keys 'made_shot' and
                'missed_shot' and values a 1 x 6 array where each entry
                is the number of shots made in the
                corresponding entry's index

            region_shooting_prob: A 1 x 6 array where each entry
                is the prob of making a shot in the region
                corresponding to the entry's index

            possession_prob: Proability of having possession of
                the ball when team is on offense (float)

            two_pt_shot_attempts: An integer of the number of 2pt
                shots taken

            two_pt_shots_made: An integer of the number of 2pt
                shots made

            three_pt_shot_attempts: An integer of the number of
                3pt shots taken

            three_pt_shots_made: An integer of the number of 3pt
                shots made

            total_points: An integer of the number of points scored

            turnovers: An integer of the total turnovers made

            passes: An integer of the total passes

            steals: An integer of the total steals

            off_rebounds: An integer of the total number of
                offensive rebounds

            def_rebounds: An integer of the total number of
                defensive rebounds

            blocks: An integer of the total number of blocks

            steals_game: Avg steals per game for specified season

            steals_poss: Avg steals per possession for specified
                season

            blocks_game: Avg blocks per game for specified season

            blocks_poss: Avg blocks per possession for specified
                season

            off_rebounds_game: Avg off_rebounds per game for
                specified season

            off_rebounds_poss: Avg off_rebounds per possession for
                specified season

            def_rebounds_game: Avg def_rebounds per game for
                specified season

            def_rebounds_poss: Avg def_rebounds per possession for
                specified season

            personal_fouls_game: Avg personal_fouls per game for
                specified season

            personal_fouls_poss: Avg personal_fouls per possession
                for specified season

            free_throw_pct: Avg free throw percentage for
                specified season

            has_possession: A boolean to indicate if player has
                possession of ball

            on_defense: A boolean to indicate if player is on
                defense

            defending_who: An int of the player_id of who the
                defended_by is defending

            on_offense: A boolean to indicate if player is on
                offense

            defended_by: An int of the player_id of who the player
                is being defended by

            poss_result_on_defense: A dict that gives the
                probability of offense player's outcome when player is defending him.
                pass, shoot, turnover

            poss_result_on_defense_reg: A 6 x 3 matrix that gives
                defensive player's region (row) and offensive player's possession outcome (column)

            def_off_region_matrix: A 6 x 6 matrix that gives
                defense player (row) vs. offense player region (col)

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

            game_idx: A boolean, 0 or 1, of which index to update
                in game_class


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
        self.region_freq_matrix = None
        self.action_freq_matrix = None
        self.shooting_freq = None
        self.shooting_prob = None
        self.region_shooting_prob = None
        self.region_shooting_freq = None
        self.possession_prob = 0
        self.two_pt_shot_attempts = 0
        self.two_pt_shots_made = 0
        self.three_pt_shot_attempts = 0
        self.three_pt_shots_made = 0
        self.total_points = 0
        self.turnovers = 0
        self.passes = 0
        self.steals = 0
        self.off_rebounds = 0
        self.def_rebounds = 0
        self.blocks = 0
        self.steals_game = 0
        self.steals_poss = 0
        self.blocks_game = 0
        self.blocks_poss = 0
        self.off_rebounds_game = 0
        self.off_rebounds_poss = 0
        self.def_rebounds_game = 0
        self.def_rebounds_poss = 0
        self.personal_fouls_game = 0
        self.personal_fouls_poss = 0
        self.free_throw_pct = 0
        self.has_possession = False
        self.on_defense = False
        self.defending_who = None
        self.on_offense = False
        self.defended_by = None
        self.poss_result_on_defense = None
        self.poss_result_on_defense_reg = None
        self.court_region = None
        self.court_coord = None
        self.game_idx = None


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
        info_list = game_player_dict[player_id]

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

        player_class_dict[player_id] = Player(
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
        player_class.two_pt_shot_attempts = 0
        player_class.two_pt_shots_made = 0
        player_class.three_pt_shot_attempts = 0
        player_class.three_pt_shots_made = 0
        player_class.total_points = 0
        player_class.turnovers = 0
        player_class.passes = 0
        player_class.steals = 0
        player_class.off_rebounds = 0
        player_class.def_rebounds = 0
        player_class.blocks = 0
        player_class.has_possession = False
        player_class.on_defense = False
        player_class.defending_who = None
        player_class.on_offense = False
        player_class.defended_by = None
        player_class.court_region = None
        player_class.court_coord = None
