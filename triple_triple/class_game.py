class Game(object):
    """
    A simulated game
    Attributes:
        teams: A dictionary with key, value {'hometeam': hometeam_id, 'awayteam': awayteam_id}
        score: An int of the total points scored in the game
        two_pt_shot_attempts:
        two_pt_shots_made:
        three_pt_shot_attempts:
        three_pt_shots_made:
        rebounds:
        off_rebounds:
        def_rebounds:
        steals:
        blocks:
        turnovers:
        passes:
        num_plays: An int of the total number of plays in the simulation
    """

    def __init__(self, hometeam_id, awayteam_id):
        self.teams = {
            'hometeam': hometeam_id,
            'awayteam': awayteam_id
        }
        self.score = [0, 0]
        self.two_pt_shot_attempts = [0, 0]
        self.two_pt_shots_made = [0, 0]
        self.three_pt_shot_attempts = [0, 0]
        self.three_pt_shots_made = [0, 0]
        self.rebounds = [0, 0]
        self.off_rebounds = [0, 0]
        self.def_rebounds = [0, 0]
        self.steals = [0, 0]
        self.blocks = [0, 0]
        self.turnovers = [0, 0]
        self.passes = [0, 0]
        self.num_plays = [0, 0]


def game_class_reset(game_class):
    game_class.score = [0, 0]
    game_class.two_pt_shot_attempts = [0, 0]
    game_class.two_pt_shots_made = [0, 0]
    game_class.three_pt_shot_attempts = [0, 0]
    game_class.three_pt_shots_made = [0, 0]
    game_class.rebounds = [0, 0]
    game_class.off_rebounds = [0, 0]
    game_class.def_rebounds = [0, 0]
    game_class.steals = [0, 0]
    game_class.blocks = [0, 0]
    game_class.turnovers = [0, 0]
    game_class.passes = [0, 0]
    game_class.num_plays = [0, 0]
