import copy
import numpy as np

from triple_triple.class_player import create_player_class_instance

from triple_triple.court_region_coord import generate_rand_regions
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

# TODO: FIX simulate play after turnover and rebound to see which team starts the play - ie. fix back and forth business.
# TODO: FIX choose_player_action to make more sense -> steals and turnover probabilities are just added for turnover prob
# TODO: FIX shot_outcome to make more sense -> prob_make = prob_make - defender's block probabilities
# TODO: Fix score in sim_offense_play. It's too redundant
# TODO: who gets rebound after missed shot

# TODO: Incorporate shot clock to force shot



# def get_simulated_coord(player_sim_reg, shooting_side):
#     coord = []
#     for i in range(len(player_sim_reg)):
#         coord.append(generate_rand_regions(player_sim_reg[i], shooting_side))
#     return coord


def who_has_possession(players_offense_dict):
    has_ball_list = filter(
        lambda player:
        players_offense_dict[player]
        .has_possession is True, players_offense_dict
        .keys()
    )
    if len(has_ball_list) == 1:
        return has_ball_list[0]
    else:
        raise ValueError('No one or multiple players have ball')


def initiate_player_has_possession(players_offense_dict):
    # make sure everyone's possession is set to False
    for player_class in players_offense_dict.values():
        player_class.has_possession = False
        player_class.on_offense = True

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
        region = get_reg_to_num('out_of_bounds')
        if shooting_side == 'right':
            coord = [96, 25]
        elif shooting_side == 'left':
            coord = [-2, 25]

    ball_class.court_region = region
    ball_class.court_coord = coord


def update_defense_params(offense_class, defender_class):
    defender_class.on_defense = True
    defender_class.defending_who = offense_class.player_id
    offense_class.defended_by = defender_class.player_id


def match_players_random(
    players_defense_dict,
    players_offense_dict,
    unmatched_players=None
):
    if unmatched_players is None:
        players_defense_dict_copy = copy.deepcopy(players_defense_dict)
        players_offense_dict_copy = copy.deepcopy(players_offense_dict)
    else:
        players_defense_dict_copy = unmatched_players[0]
        players_offense_dict_copy = unmatched_players[1]

    off_players_list = list(players_offense_dict.values())

    for defender in players_defense_dict_copy.values():
        off_player = off_players_list[0]
        players_defense_dict[defender.player_id].court_region = \
            players_offense_dict[off_player.player_id].court_region
        players_defense_dict[defender.player_id].court_coord = \
            players_offense_dict[off_player.player_id].court_coord

        # update on_defense and defender status
        update_defense_params(
            offense_class=players_offense_dict[off_player.player_id],
            defender_class=players_defense_dict[defender.player_id]
        )

        # remove the matched players
        off_players_list.pop(0)
        del players_defense_dict_copy[defender.player_id]
        del players_offense_dict_copy[off_player.player_id]

    return [players_defense_dict_copy, players_offense_dict_copy]


def closest_height_to_defender(defender_class, players_offense_dict):
    players = list(players_offense_dict.values())
    height_from_defender = [
        player.height - defender_class.height for player in players
    ]
    idx_closest_player = np.abs(np.array(height_from_defender)).argmin()

    return players[idx_closest_player].player_id


def match_players_height(
    players_defense_dict,
    players_offense_dict,
    unmatched_players=None
):
    if unmatched_players is None:
        players_defense_dict_copy = copy.deepcopy(players_defense_dict)
        players_offense_dict_copy = copy.deepcopy(players_offense_dict)
    else:
        players_defense_dict_copy = unmatched_players[0]
        players_offense_dict_copy = unmatched_players[1]

    for defender in players_defense_dict_copy.values():
        closest_off_player_id = closest_height_to_defender(
            defender_class=defender, players_offense_dict=players_offense_dict_copy
        )
        players_defense_dict[defender.player_id].court_region = \
            players_offense_dict[closest_off_player_id].court_region
        players_defense_dict[defender.player_id].court_coord = \
            players_offense_dict[closest_off_player_id].court_coord

        # update on_defense and defender status
        update_defense_params(
            offense_class=players_offense_dict[closest_off_player_id],
            defender_class=players_defense_dict[defender.player_id]
        )

        # remove the matched players
        del players_defense_dict_copy[defender.player_id]
        del players_offense_dict_copy[closest_off_player_id]

    return [players_defense_dict_copy, players_offense_dict_copy]


def match_players_same_position(
    players_defense_dict,
    players_offense_dict,
    unmatched_players=None
):
    if unmatched_players is None:
        players_defense_dict_copy = copy.deepcopy(players_defense_dict)
        players_offense_dict_copy = copy.deepcopy(players_offense_dict)
    else:
        players_defense_dict_copy = unmatched_players[0]
        players_offense_dict_copy = unmatched_players[1]

    # match players using position
    for defender in players_defense_dict_copy.values():
        defender_id = defender.player_id
        # break up position in to list for cases such as 'F-G'
        defender_position = list(defender.position)
        try:
            match_player_id = next(
                player_class.player_id
                for player_class
                in players_offense_dict_copy.values()
                if not set(
                    list(player_class.position)).isdisjoint(defender_position)
                )
            players_defense_dict[defender_id].court_region = \
                players_offense_dict[match_player_id].court_region
            players_defense_dict[defender_id].court_coord = \
                players_offense_dict[match_player_id].court_coord

            # update on_defense and defender status
            update_defense_params(
                offense_class=players_offense_dict[match_player_id],
                defender_class=players_defense_dict[defender.player_id]
            )
            # remove the matched players
            del players_offense_dict_copy[match_player_id]
            del players_defense_dict_copy[defender_id]
        except:
            continue

    return [players_defense_dict_copy, players_offense_dict_copy]


def initiate_offense_player_positions(players_offense_dict, shooting_side, num_reg=6):
    # update on_offense status
    for player_class in players_offense_dict.values():
        player_class.on_offense = True

    # update everyone's position
    update_offense_player_positions(
        players_offense_dict=players_offense_dict,
        shooting_side=shooting_side,
        num_reg=6
    )

    # update player with ball to 'out of bounds' <--> 5
    has_ball = who_has_possession(players_offense_dict)

    players_offense_dict[has_ball]\
        .court_region = get_reg_to_num('out_of_bounds')
    players_offense_dict[has_ball]\
        .court_coord = generate_rand_regions(
        court_region_num=players_offense_dict[has_ball].court_region,
        shooting_side=shooting_side
    )


def initiate_defense_player_positions(
    players_defense_dict,
    players_offense_dict
):
    # match players by position
    # unmatched_players = [players_defense_dict_copy, players_offense_dict_copy]
    unmatched_players = \
        match_players_same_position(
            players_defense_dict=players_defense_dict,
            players_offense_dict=players_offense_dict,
            unmatched_players=None
        )

    # match remaining players by height
    unmatched_players = \
        match_players_height(
            players_defense_dict=players_defense_dict,
            players_offense_dict=players_offense_dict,
            unmatched_players=unmatched_players
        )

    # match remaining players randomly
    unmatched_players = \
        match_players_random(
            players_defense_dict=players_defense_dict,
            players_offense_dict=players_offense_dict,
            unmatched_players=unmatched_players
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


def update_offense_player_positions(
    players_offense_dict,
    shooting_side,
    num_reg=6
):
    # initial has_ball puts player out of bounds
    region_list = ['paint', 'mid_range', 'key', 'perimeter']
    pos_available = map(get_reg_to_num, region_list)

    for player_class in players_offense_dict.values():
        current_region = player_class.court_region

        if current_region is None:
            try:
                reg = np.random.choice(pos_available)
                pos_available.remove(reg)
            except:
                reg = np.random.choice(
                    map(get_reg_to_num, region_list)
                )
            player_class.court_region = reg

        else:
            current_region = player_class.court_region

            # update to new region
            player_class.court_region = np.random.choice(
                a=np.arange(num_reg),
                p=player_class.region_prob_matrix[current_region],
            )

        player_class.court_coord = generate_rand_regions(
            court_region_num=player_class.court_region,
            shooting_side=shooting_side
        )


def update_defense_player_positions(
    players_defense_dict,
    players_offense_dict
):
    for defender in players_defense_dict.values():
        off_player_id = defender.defending_who
        defender.court_region = players_offense_dict[off_player_id].court_region
        defender.court_coord = players_offense_dict[off_player_id].court_coord


def dist_two_points(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_closest_to_ball(players_dict, ball_class):
    player_id_list = []
    dist_to_ball = []

    for player_class in players_dict.values():
        player_id_list.append(player_class.player_id)
        dist_to_ball.append(
            dist_two_points(
                point1=ball_class.court_coord,
                point2=player_class.court_coord
            )
        )
    dist_to_ball = np.array(dist_to_ball)
    min_dist_idx = np.where(
        dist_to_ball == dist_to_ball.min()
    )[0]

    return [player_id_list[i] for i in min_dist_idx]


def who_gets_rebound(
    players_offense_dict,
    players_defense_dict,
    ball_class
):
    closest_off_players = get_closest_to_ball(
        players_dict=players_offense_dict,
        ball_class=ball_class
    )
    closest_def_players = get_closest_to_ball(
        players_dict=players_defense_dict,
        ball_class=ball_class
    )
    off_reb_prob = [players_offense_dict[player].off_rebounds_poss for player in closest_off_players]
    def_reb_prob = [players_defense_dict[player].def_rebounds_poss for player in closest_def_players]

    # scale combined probability array
    prob_array = np.array(off_reb_prob + def_reb_prob) / sum(off_reb_prob + def_reb_prob)

    rebounder_id = np.random.choice(
        a=closest_off_players + closest_def_players,
        p=prob_array
    )
    try:
        return players_defense_dict[rebounder_id]
    except:
        return players_offense_dict[rebounder_id]


def choose_player_action(
    has_ball_player_class,
    defender_class,
    num_actions=3
):
    current_region = has_ball_player_class.court_region
    action_prob = copy.deepcopy(
        has_ball_player_class
        .action_prob_matrix[current_region]
    )
    # action in [0, 1, 2] <---> pass, shoot, turnover

    # account for steals
    action_prob[2] += defender_class.steals_poss

    # account for blocks
    action_prob[1] -= defender_class.blocks_poss

    # find new action_prob array
    new_action_prob = action_prob / action_prob.sum()

    return np.random.choice(
        a=np.arange(num_actions),
        p=new_action_prob
    )


def shot_outcome(
    has_ball_player_class,
    defender_class,
    game_class,
    idx
):
    shooting_region = has_ball_player_class.court_region
    # determine if blocked or not
    # 0 = blocked, 1 = not blocked
    prob_block = defender_class.blocks_poss
    block_outcome = np.random.choice(
        a=np.arange(2),
        p=[prob_block, 1 - prob_block]
    )

    # if blocked, outcome = miss = 0
    if block_outcome == 0:
        outcome = 0
        # update defender and game stats
        defender_class.blocks += 1
        game_class.blocks[idx] += 1

    elif block_outcome == 1:
        # 0 = miss, 1 = make
        # incorporate defender's block proability
        prob_make = (has_ball_player_class.region_shooting_prob[shooting_region] -
                     defender_class.blocks_poss)

        outcome = np.random.choice(
            a=np.arange(2),
            p=[1 - prob_make, prob_make]
        )

    check_3pt = shooting_region in \
        [get_reg_to_num('perimeter'), get_reg_to_num('back_court')]

    return check_3pt, outcome


def update_shot_outcome(has_ball_player_class, game_class, check_3pt, outcome, idx):
    if check_3pt:
        has_ball_player_class.three_pt_shot_attempts += 1
        game_class.three_pt_shot_attempts[idx] += 1

        if outcome == 1:
            has_ball_player_class.three_pt_shots_made += 1
            game_class.three_pt_shots_made[idx] += 1
            has_ball_player_class.total_points += 3
            game_class.score[idx] += 3

    else:
        has_ball_player_class.two_pt_shot_attempts += 1
        game_class.two_pt_shot_attempts[idx] += 1

        if outcome == 1:
            has_ball_player_class.two_pt_shots_made += 1
            game_class.two_pt_shots_made[idx] += 1
            has_ball_player_class.total_points += 2
            game_class.score[idx] += 2


def update_rebound(players_offense_dict, players_defense_dict, game_class, idx):
    rebounder_class = who_gets_rebound(
        players_offense_dict=players_offense_dict,
        players_defense_dict=players_defense_dict,
        ball_class=ball_class,
    )

    if rebounder_class.on_defense:
        rebounder_class.def_rebounds += 1
        game_class.def_rebounds[idx] += 1

    else:
        rebounder_class.off_rebounds += 1
        game_class.off_rebounds[idx] += 1


def check_turnover_is_steal(
    defender_class,
    game_class,
    idx
):
    # determine if turnover action is steal
    # 0 = steal, 1 = not a steal
    turnover_action = np.random.choice(
        a=[True, False],
        p=[defender_class.steals_poss, 1 - defender_class.steals_poss]
    )

    if turnover_action:
        defender_class.steals += 1
        game_class.steals[idx] += 1

    return turnover_action


def switch_possession(players_offense_dict, players_defense_dict):
    for player_class in players_offense_dict.values():
        player_class.has_possession = False
        player_class.on_defense = True
        player_class.on_offense = False

    for player_class in players_defense_dict.values():
        player_class.on_defense = False
        player_class.on_offense = True
    
        

def sim_offense_play(
    players_offense_dict,
    players_defense_dict,
    game_class,
    shooting_side,
    start_play,
    player_action,
    idx
):
    if start_play:
        start_play = False
        initiate_player_has_possession(players_offense_dict)
        initiate_offense_player_positions(
            players_offense_dict=players_offense_dict,
            shooting_side=shooting_side,
            num_reg=6
        )
        initiate_defense_player_positions(
            players_defense_dict=players_defense_dict,
            players_offense_dict=players_offense_dict
        )
        update_ball_position(
            players_offense_dict=players_offense_dict,
            ball_class=ball_class,
            shooting_side=shooting_side,
            action=player_action
        )

    else:
        # update play number
        game_class.num_plays[idx] += 1
        # determine who has ball
        has_ball = who_has_possession(players_offense_dict)
        # determine who he is defended by
        defender_id = players_offense_dict[has_ball].defended_by
        # determine his action
        player_action = choose_player_action(
            has_ball_player_class=players_offense_dict[has_ball],
            defender_class=players_defense_dict[defender_id],
            num_actions=3
        )
        # pass
        if player_action == 0:
            game_class.passes[idx] += 1
            players_offense_dict[has_ball].passes += 1
            start_play = False
            update_has_possession(players_offense_dict)
            update_offense_player_positions(
                players_offense_dict=players_offense_dict,
                shooting_side=shooting_side,
                num_reg=6
            )
            update_defense_player_positions(
                players_defense_dict=players_defense_dict,
                players_offense_dict=players_offense_dict
            )
            update_ball_position(
                players_offense_dict=players_offense_dict,
                action=player_action,
                shooting_side=shooting_side
            )

        # shoot
        elif player_action == 1:
            check_3pt, outcome = shot_outcome(
                has_ball_player_class=players_offense_dict[has_ball],
                defender_class=players_defense_dict[defender_id],
                game_class=game_class,
                idx=idx
            )
            update_shot_outcome(
                has_ball_player_class=players_offense_dict[has_ball],
                game_class=game_class,
                check_3pt=check_3pt,
                outcome=outcome,
                idx=idx
            )
            # update rebound if shot is missed
            if outcome == 0:
                update_rebound(
                    players_offense_dict=players_offense_dict,
                    players_defense_dict=players_defense_dict,
                    game_class=game_class,
                    idx=idx
                )
            start_play = True
            # update ball tp rim
            update_ball_position(
                players_offense_dict=players_offense_dict,
                action=player_action,
                shooting_side=shooting_side
            )
            update_defense_player_positions(
                players_defense_dict=players_defense_dict,
                players_offense_dict=players_offense_dict
            )

            # change player's possession to False
            players_offense_dict[has_ball].has_possession = False

        # turnover
        elif player_action == 2:
            game_class.turnovers[idx] += 1
            players_offense_dict[has_ball].turnovers += 1

            # check if steal
            turnover_action = check_turnover_is_steal(
                defender_class=players_defense_dict[defender_id],
                game_class=game_class,
                idx=idx
            )

            if not turnover_action:
                start_play = True
                # update out of bounds
                update_ball_position(
                    players_offense_dict=players_offense_dict,
                    action=player_action,
                    shooting_side=shooting_side
                )

                # change player's possession to False
                players_offense_dict[has_ball].has_possession = False

    return player_action, start_play


def add_sim_coord_to_dict(players_dict, sim_coord_dict):
    for player, player_class in players_dict.items():
        sim_coord_dict.setdefault(player, []).append(player_class.court_coord)

    return sim_coord_dict


def create_sim_coord_dict(
    players_offense_dict,
    players_defense_dict,
    game_class,
    shooting_side,
    num_sim
):
    # simulate the play
    start_play = True
    player_action = None
    sim_coord_dict = {}

    # get coordinates
    for i in range(num_sim):
        player_action, start_play = sim_offense_play(
            players_offense_dict=players_offense_dict,
            players_defense_dict=players_defense_dict,
            game_class=game_class,
            shooting_side=shooting_side,
            start_play=start_play,
            player_action=player_action,
        )

        sim_coord_dict = add_sim_coord_to_dict(
            players_dict=players_offense_dict,
            sim_coord_dict=sim_coord_dict
        )

    return sim_coord_dict
