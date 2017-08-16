class MockPlayer(object):

    def __init__(self, name, player_id, position):
        self.name = name
        self.player_id = player_id
        self.team_id = 0
        self.jersey = 0
        self.position = position
        self.height = 0
        self.weight = 0
        self.region_prob_matrix = None
        self.action_prob_matrix = None
        self.shooting_prob = None
        self.region_shooting_prob = None
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


def create_player_instances_dict(off_or_def):
    player_class_dict = {}
    positions = ['X', 'Y', 'Z']
    for player in [0, 1, 2]:
        if off_or_def == 'off':
            player_class_dict[player] = MockPlayer(
                name='off' + str(player),
                player_id=player,
                position=positions[player],
            )

            player_class_dict[player].on_offense = True
            player_class_dict[player].on_defense = False
            player_class_dict[player].defended_by = 'def' + str(player)

        elif off_or_def == 'def':
            player_class_dict[player] = MockPlayer(
                name='def' + str(player),
                player_id=player,
                position=positions[player],
            )

            player_class_dict[player].on_offense = False
            player_class_dict[player].on_defense = True
            player_class_dict[player].defending_who = 'off' + str(player)

    return player_class_dict


def create_ball_class():
    return MockPlayer(name='ball', player_id=-1, position=-1)
