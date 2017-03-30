import copy
import numpy as np

from triple_triple.class_player import create_player_class_instance

from triple_triple.court_region_coord import generate_rand_positions
from triple_triple.startup_data import get_game_player_dict
from triple_triple.prob_player_possessions import (
    relative_player_possession_prob,
    get_reg_to_num
)

game_player_dict = get_game_player_dict()
# this is weird since this will only have one element
ball_class_dict = create_player_class_instance(
    player_list=[-1],
    game_player_dict=game_player_dict,
)

ball_class = ball_class_dict[-1]

# TODO: in sim_offense_play, keep track of made/missed shots,
# TODO: Fix score in sim_offense_play. It's too redundant
# TODO:  who gets rebound after missed shot
# TODO: Perhaps change update_player_positions so that player positions are unique
# TODO: Incorporate shot clock to force shot
# TODO: This is messier than it needs to be


def get_simulated_coord(player_sim_reg, shooting_side):
    coord = []
    for i in range(len(player_sim_reg)):
        coord.append(generate_rand_positions(player_sim_reg[i], shooting_side))
    return coord


def who_has_possession(players_offense_dict):
    has_ball_list = filter(
        lambda player: players_offense_dict[player].has_possession is True, players_offense_dict.keys()
    )
    if len(has_ball_list) == 1:
        return has_ball_list[0]
    else:
        raise ValueError('No one or multiple players have ball')


def initiate_player_has_possession(players_offense_dict):
    # make sure everyone's possession is set to False
    for player_class in players_offense_dict.values():
        player_class.has_possession = False

    # choose player with possession
    player_list, prob = relative_player_possession_prob(players_offense_dict)
    has_poss = np.random.choice(
        a=np.arange(len(player_list)),
        p=prob
    )

    # update player possession to True
    players_offense_dict[player_list[has_poss]]\
        .has_possession = True


def update_ball_position(
    players_offense_dict,
    ball_class=ball_class,
    shooting_side=None,
    action=None
):
    # result of a pass
    if action == 0 or action is None:
        has_ball = who_has_possession(players_offense_dict)
        region = players_offense_dict[has_ball].court_region
        coord = players_offense_dict[has_ball].court_coord

    # action is a shot
    elif action == 1:
        region = get_reg_to_num('paint')
        if shooting_side == 'right':
            coord = [88.75, 25]
        elif shooting_side == 'left':
            coord = [5.25, 25]

    # action is a turnover
    elif action == 2:
        region = get_reg_to_num('out of bounds')
        if shooting_side == 'right':
            coord = [96, 25]
        elif shooting_side == 'left':
            coord = [-2, 25]

    ball_class.court_region = region
    ball_class.court_coord = coord


def initiate_player_positions(players_offense_dict, shooting_side, num_reg=6):
    # update everyone's position
    update_player_positions(
        players_offense_dict=players_offense_dict,
        shooting_side=shooting_side,
        num_reg=6
    )

    # update player with ball to 'out of bounds' <--> 3
    has_ball = who_has_possession(players_offense_dict)

    players_offense_dict[has_ball]\
        .court_region = get_reg_to_num('out of bounds')
    players_offense_dict[has_ball]\
        .court_coord = generate_rand_positions(
        pos_num=players_offense_dict[has_ball].court_region,
        shooting_side=shooting_side
    )


def update_has_possession(players_offense_dict, ball_class=ball_class):
    old_has_ball = who_has_possession(players_offense_dict)

    players_without_ball = [
        player for player in players_offense_dict.keys()
        if player != old_has_ball
    ]

    # choose new player randomly
    # update has_possession of all old/new has_ball players
    players_offense_dict[old_has_ball].has_possession = False
    new_has_ball = players_without_ball[
        np.random.choice(
            a=np.arange(len(players_without_ball))
        )
    ]
    players_offense_dict[new_has_ball].has_possession = True

    # update ball region/coordinates
    update_ball_position(players_offense_dict, ball_class=ball_class)


def update_player_positions(
    players_offense_dict,
    shooting_side,
    num_reg=6
):

    for player_class in players_offense_dict.values():
        current_region = player_class.court_region

        if current_region is None:
            current_region = np.random.choice(a=np.arange(num_reg))
        else:
            current_region = player_class.court_region
        # update to new region
        player_class.court_region = np.random.choice(
            a=np.arange(num_reg),
            p=player_class.region_prob_matrix[current_region],
        )

        player_class.court_coord = generate_rand_positions(
            pos_num=player_class.court_region,
            shooting_side=shooting_side
        )


def choose_player_action(has_ball_player_class, num_actions=3):
    current_region = has_ball_player_class.court_region
    prob = has_ball_player_class.action_prob_matrix[current_region]
    # action in [0, 1, 2] <---> pass, shoot, turnover
    return np.random.choice(
        a=np.arange(num_actions),
        p=prob
    )


def shot_outcome(player_class):
    shooting_region = player_class.court_region
    if shooting_region == 5:
        add_score = 3
    else:
        add_score = 2

    # determine if shot made or miss
    # 0 = miss, 1 = make
    prob_array = [
        1 - player_class.region_shooting_prob[shooting_region],
        player_class.region_shooting_prob[shooting_region]
    ]

    outcome = np.random.choice(
        a=np.arange(2),
        p=prob_array
    )

    if outcome == 0:
        add_score = 0
    else:
        player_class.shots_made += 1

    player_class.shot_attempts += 1
    player_class.total_points += add_score

    return add_score


def sim_offense_play(
    players_offense_dict,
    shooting_side,
    start_play,
    player_action,
    score
):
    if start_play:
        start_play = False
        initiate_player_has_possession(players_offense_dict)
        initiate_player_positions(
            players_offense_dict=players_offense_dict,
            shooting_side='right',
            num_reg=6
        )

        update_ball_position(
            players_offense_dict=players_offense_dict,
            ball_class=ball_class,
            shooting_side=shooting_side,
            action=player_action
        )

    else:
        has_ball = who_has_possession(players_offense_dict)
        # determine his action
        player_action = choose_player_action(players_offense_dict[has_ball])
        # pass
        if player_action == 0:
            players_offense_dict[has_ball].passes += 1
            start_play = False
            update_has_possession(players_offense_dict)
            update_player_positions(
                players_offense_dict,
                shooting_side,
                num_reg=6
            )
            update_ball_position(
                players_offense_dict=players_offense_dict,
                action=player_action,
                shooting_side=shooting_side
            )

        # shoot
        elif player_action == 1:
            score += shot_outcome(players_offense_dict[has_ball])
            start_play = True
            # update ball tp rim
            update_ball_position(
                players_offense_dict=players_offense_dict,
                action=player_action,
                shooting_side=shooting_side
            )

            # change player's possession to False
            players_offense_dict[has_ball].has_possession = False

        # turnover
        elif player_action == 2:
            players_offense_dict[has_ball].turnovers += 1
            start_play = True
            # update out of bounds
            update_ball_position(
                players_offense_dict=players_offense_dict,
                action=player_action,
                shooting_side=shooting_side
            )

            # change player's possession to False
            players_offense_dict[has_ball].has_possession = False

    return player_action, start_play, score


def add_sim_coord_to_dict(players_dict, sim_coord_dict):
    for player, player_class in players_dict.items():
        sim_coord_dict.setdefault(player, []).append(player_class.court_coord)

    return sim_coord_dict


def create_sim_coord_dict(players_offense_dict, num_sim):
    # simulate the play
    start_play = True
    player_action = None
    sim_coord_dict = {}

    # get coordinates
    for i in range(num_sim):
        player_action, start_play, score = sim_offense_play(
            players_offense_dict=players_offense_dict,
            shooting_side='right',
            start_play=start_play,
            player_action=player_action
        )

        sim_coord_dict = add_sim_coord_to_dict(
            players_dict=players_offense_dict,
            sim_coord_dict=sim_coord_dict
        )

    return sim_coord_dict
