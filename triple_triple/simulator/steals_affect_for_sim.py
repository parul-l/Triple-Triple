import numpy as np


def steals_affect_on_turnover(turnover_prob, steals_prob):
    return turnover_prob + steals_prob


def update_turnover_params(has_ball_class, game_class, off_game_idx):
    game_class.turnovers[off_game_idx] += 1
    has_ball_class.turnovers += 1
    has_ball_class.has_possession = False


def check_turnover_is_steal(
    defender_class,
    game_class,
):
    # determine if turnover action is steal
    turnover_steal = np.random.choice(
        a=[True, False],
        p=[defender_class.steals_poss, 1 - defender_class.steals_poss]
    )

    if turnover_steal:
        defender_class.steals += 1
        game_class.steals[defender_class.game_idx] += 1
        defender_class.has_possession = True

    return turnover_steal
