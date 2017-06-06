import copy
import pandas as pd
import numpy as np

from triple_triple.class_player import create_player_class_instance

from triple_triple.court_region_coord import generate_rand_regions
from triple_triple.simulator.match_defenders_for_sim import (
    initiate_defense_player_positions,
    update_defense_player_positions
)
from triple_triple.simulator.blocks_affect_for_sim import (
    blocks_affect_on_taking_shot,
    blocks_affect_on_making_shot
)
from triple_triple.simulator.steals_affect_for_sim import (
    steals_affect_on_turnover,
    update_turnover_params,
    check_turnover_is_steal
)
from triple_triple.simulator.rebounds_for_sim import update_rebound_params


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


# TODO: FIX choose_player_action to make more sense -> steals and turnover probabilities are just added for turnover prob
# TODO: FIX shot_outcome to make more sense -> prob_make = prob_make - defender's block probabilities
# TODO: Incorporate shot clock to force shot
# TODO: Fix try/except in who_gets_rebound
# TODO: Get player coord simulator working


def update_play_number(game_class, off_game_idx):
    game_class.num_plays[off_game_idx] += 1


def switch_team_possession(teams_list):
    players_offense_dict, players_defense_dict = teams_list[0], teams_list[1]
    for player_class in players_offense_dict.values():
        player_class.has_possession = False
        player_class.on_defense = True
        player_class.on_offense = False
        player_class.defending_who = player_class.defended_by
        player_class.defended_by = None

    for player_class in players_defense_dict.values():
        player_class.on_defense = False
        player_class.on_offense = True
        player_class.defended_by = player_class.defending_who
        player_class.defending_who = None

    return [teams_list[1], teams_list[0]]


def switch_shooting_side(shooting_side_list):
    return [shooting_side_list[1], shooting_side_list[0]]


def switch_possession_params(teams_list, shooting_side_list):
    teams_list = switch_team_possession(teams_list=teams_list)
    shooting_side_list = \
        switch_shooting_side(shooting_side_list=shooting_side_list)

    return teams_list, shooting_side_list


def who_has_possession(players_offense_dict):
    has_ball_list = filter(
        lambda player:
        players_offense_dict[player]
        .has_possession is True, players_offense_dict
        .keys()
    )
    if len(has_ball_list) == 1:
        return players_offense_dict[has_ball_list[0]]
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
    shooting_side,
    has_ball_class=None,
    out_of_bounds=False,
    ball_class=ball_class
):
    if out_of_bounds:
        region = get_reg_to_num('out_of_bounds')
        if shooting_side == 'right':
            coord = [96, 25]
        elif shooting_side == 'left':
            coord = [-2, 25]

    elif has_ball_class is None:
        region = get_reg_to_num('paint')
        # update coordinates to the rim
        if shooting_side == 'right':
            coord = [88.75, 25]
        elif shooting_side == 'left':
            coord = [5.25, 25]

    else:
        region = has_ball_class.court_region
        coord = has_ball_class.court_coord

    ball_class.court_region = region
    ball_class.court_coord = coord


def initiate_offense_player_positions(
    players_offense_dict,
    shooting_side,
    num_reg=6
):
    # update on_offense status
    for player_class in players_offense_dict.values():
        player_class.on_offense = True

    # update everyone's position
    update_offense_player_positions(
        players_offense_dict=players_offense_dict,
        shooting_side=shooting_side,
        num_reg=6
    )

    # update player with ball to 'out of bounds'
    has_ball_class = who_has_possession(players_offense_dict)

    has_ball_class.court_region = get_reg_to_num('out_of_bounds')
    has_ball_class.court_coord = generate_rand_regions(
        court_region_num=has_ball_class.court_region,
        shooting_side=shooting_side
    )

    # update ball position to out_of_bounds
    update_ball_position(
        shooting_side=shooting_side,
        out_of_bounds=True
    )


def initiate_start_of_play(
    teams_list,
    shooting_side,
    ball_class
):
    players_offense_dict = teams_list[0]

    initiate_player_has_possession(players_offense_dict)
    initiate_offense_player_positions(
        players_offense_dict=players_offense_dict,
        shooting_side=shooting_side,
        num_reg=6
    )
    initiate_defense_player_positions(
        teams_list=teams_list
    )

    has_ball_class = who_has_possession(players_offense_dict)
    update_ball_position(
        shooting_side=shooting_side,
        has_ball_class=has_ball_class,
        ball_class=ball_class,
    )
    return has_ball_class


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


def update_player_movement(teams_list, shooting_side):
    update_offense_player_positions(
        players_offense_dict=teams_list[0],
        shooting_side=shooting_side,
        num_reg=6
    )
    update_defense_player_positions(teams_list=teams_list)


def update_has_possession_after_pass(
    players_offense_dict,
    ball_class=ball_class
):
    old_has_ball = who_has_possession(players_offense_dict)

    players_without_ball = [
        player for player in players_offense_dict.keys()
        if player != old_has_ball
    ]

    # choose new player randomly
    # update has_possession of all old/new has_ball players
    new_has_ball = players_without_ball[
        np.random.choice(a=np.arange(len(players_without_ball)))
    ]
    old_has_ball.has_possession = False
    players_offense_dict[new_has_ball].has_possession = True

    return players_offense_dict[new_has_ball]


def update_pass_params(game_class, off_game_idx, has_ball_class):
    game_class.passes[off_game_idx] += 1
    has_ball_class.passes += 1


def player_blocked_possession_switch(defender_class, teams_list, shooting_side_list):
    # switch team possession
    teams_list, shooting_side_list = switch_possession_params(
        teams_list=teams_list,
        shooting_side_list=shooting_side_list,
    )

    # switch player possession
    defender_class.has_possession = True
    update_ball_position(
        shooting_side=shooting_side_list[0],
        has_ball_class=defender_class
    )
    return defender_class.player_id, teams_list, shooting_side_list


def update_rebound_missed_shot(teams_list, game_class, shooting_side_list):
    rebounder_class = update_rebound_params(
        teams_list=teams_list,
        game_class=game_class,
        ball_class=ball_class
    )

    if rebounder_class.on_defense:
        # switch team possession
        teams_list, shooting_side_list = switch_possession_params(
            teams_list=teams_list,
            shooting_side_list=shooting_side_list,
        )

    update_ball_position(
        shooting_side=shooting_side_list[0],
        has_ball_class=rebounder_class
    )

    return rebounder_class.player_id, teams_list, shooting_side_list


def update_ball_stolen(defender_class, shooting_side):
    defender_class.has_possession = True
    update_ball_position(
        shooting_side=shooting_side,
        has_ball_class=defender_class
    )


def choose_player_action(
    has_ball_class,
    defender_class,
    num_actions=3
):
    current_region = has_ball_class.court_region
    action_prob = copy.deepcopy(
        has_ball_class
        .action_prob_matrix[current_region]
    )
    # action in [0, 1, 2] <---> pass, shoot, turnover

    # account for steals
    action_prob[2] = steals_affect_on_turnover(
        turnover_prob=action_prob[2], steals_prob=defender_class.steals_poss
    )

    # account for blocks
    action_prob[1] = blocks_affect_on_taking_shot(
        shot_prob=action_prob[1],
        blocks_prob=defender_class.blocks_poss
    )
    # find new action_prob array
    new_action_prob = action_prob / action_prob.sum()

    return np.random.choice(
        a=np.arange(num_actions),
        p=new_action_prob
    )


def get_shot_outcome(
    has_ball_class,
    defender_class,
    game_class,
):
    shooting_region = has_ball_class.court_region
    # determine if blocked or not
    # 0 = blocked, 1 = not blocked
    prob_block = defender_class.blocks_poss
    block_outcome = np.random.choice(
        a=np.arange(2),
        p=[prob_block, 1 - prob_block]
    )

    # if blocked, outcome = miss = 0
    if block_outcome == 0:
        shot_outcome = 0
        # update defender and game stats
        defender_class.blocks += 1
        game_class.blocks[defender_class.game_idx] += 1

    elif block_outcome == 1:
        # determine if shot is made: 0 = miss, 1 = make
        # incorporate defender's block proability
        prob_make = blocks_affect_on_making_shot(
            shot_prob=has_ball_class.region_shooting_prob[shooting_region],
            blocks_prob=defender_class.blocks_poss
        )

        shot_outcome = np.random.choice(
            a=np.arange(2),
            p=[1 - prob_make, prob_make]
        )

    check_3pt = shooting_region in \
        [get_reg_to_num('perimeter'), get_reg_to_num('back_court')]

    return check_3pt, shot_outcome, block_outcome


def update_shot_outcome_params(has_ball_class, game_class, check_3pt, shot_outcome):
    has_ball_class.has_possession = False

    has_ball_game_idx = has_ball_class.game_idx

    if check_3pt:
        has_ball_class.three_pt_shot_attempts += 1
        game_class.three_pt_shot_attempts[has_ball_game_idx] += 1

        if shot_outcome == 1:
            has_ball_class.three_pt_shots_made += 1
            game_class.three_pt_shots_made[has_ball_game_idx] += 1
            has_ball_class.total_points += 3
            game_class.score[has_ball_game_idx] += 3

    else:
        has_ball_class.two_pt_shot_attempts += 1
        game_class.two_pt_shot_attempts[has_ball_game_idx] += 1

        if shot_outcome == 1:
            has_ball_class.two_pt_shots_made += 1
            game_class.two_pt_shots_made[has_ball_game_idx] += 1
            has_ball_class.total_points += 2
            game_class.score[has_ball_game_idx] += 2


def sim_action(
    teams_list,
    game_class,
    shooting_side_list,
    start_play
):
    player_action = None
    block_outcome = None
    rebounder_id = None
    shot_outcome = None
    turnover_steal = None

    shooting_side = shooting_side_list[0]
    players_offense_dict, players_defense_dict = teams_list[0], teams_list[1]

    if start_play:
        start_play = False
        has_ball_class = initiate_start_of_play(
            teams_list=teams_list,
            shooting_side=shooting_side,
            ball_class=ball_class
        )

    else:
        # determine who has ball and his defender
        has_ball_class = who_has_possession(players_offense_dict)
        defender_class = players_defense_dict[has_ball_class.defended_by]

        # update player positions
        update_player_movement(teams_list=teams_list, shooting_side=shooting_side)

        off_game_idx = has_ball_class.game_idx
        # update play number
        update_play_number(
            game_class=game_class,
            off_game_idx=off_game_idx
        )

        # determine his action
        player_action = choose_player_action(
            has_ball_class=has_ball_class,
            defender_class=defender_class,
            num_actions=3
        )

        # pass
        if player_action == 0:
            start_play = False

            update_pass_params(
                game_class=game_class,
                off_game_idx=off_game_idx,
                has_ball_class=has_ball_class
            )

            has_ball_class = update_has_possession_after_pass(
                players_offense_dict=players_offense_dict
            )

            update_ball_position(
                shooting_side=shooting_side,
                has_ball_class=has_ball_class
            )

        # shoot
        elif player_action == 1:
            check_3pt, shot_outcome, block_outcome = get_shot_outcome(
                has_ball_class=has_ball_class,
                defender_class=defender_class,
                game_class=game_class
            )
            update_shot_outcome_params(
                has_ball_class=has_ball_class,
                game_class=game_class,
                check_3pt=check_3pt,
                shot_outcome=shot_outcome
            )

            # if blocked, possession switched to defender
            if block_outcome == 0:
                start_play = False

                blocker_id, teams_list, shooting_side_list = player_blocked_possession_switch(
                    defender_class=defender_class,
                    teams_list=teams_list,
                    shooting_side_list=shooting_side_list)

            # if not blocked
            elif block_outcome == 1:
                # update ball to rim
                update_ball_position(
                    shooting_side=shooting_side,
                    has_ball_class=None
                )

                # if not blocked and shot is missed
                if shot_outcome == 0:
                    start_play = False
                    # update rebound if shot is missed
                    rebounder_id, teams_list, shooting_side_list = update_rebound_missed_shot(
                        teams_list=teams_list,
                        game_class=game_class,
                        shooting_side_list=shooting_side_list
                    )

                # if not blocked and shot is made
                elif shot_outcome == 1:
                    start_play = True
                    # switch possession
                    teams_list, shooting_side_list = switch_possession_params(
                        teams_list=teams_list,
                        shooting_side_list=shooting_side_list,
                    )

        # turnover
        elif player_action == 2:
            update_turnover_params(
                has_ball_class=has_ball_class,
                game_class=game_class,
                off_game_idx=off_game_idx,
            )
            # check if steal (True/False)
            turnover_steal = check_turnover_is_steal(
                defender_class=defender_class,
                game_class=game_class
            )

            if turnover_steal:
                start_play = False
                update_ball_stolen(
                    defender_class=defender_class,
                    shooting_side=shooting_side
                )

            if not turnover_steal:
                start_play = True
                # update ball out of bounds
                update_ball_position(
                    shooting_side=shooting_side,
                    out_of_bounds=True
                )
            # switch possession
            teams_list, shooting_side_list = switch_possession_params(
                teams_list=teams_list,
                shooting_side_list=shooting_side_list,
            )

    return (
        start_play,
        teams_list,
        shooting_side_list,
        player_action,
        block_outcome,
        rebounder_id,
        shot_outcome,
        turnover_steal,
        has_ball_class.player_id
    )


def update_data_df(
    df_data,
    start_play,
    has_ball_player_id,
    player_action,
    block_outcome,
    rebounder_id,
    shot_outcome,
    turnover_steal,
):

    data_list = [
        start_play,
        has_ball_player_id,
        player_action,
        block_outcome,
        rebounder_id,
        shot_outcome,
        turnover_steal,
    ]

    df_data.loc[len(df_data)] = data_list

    return df_data


def sim_plays(
    num_sim,
    teams_list,
    game_class,
):
    # create dataframe to collet actions
    column_headers = [
        'start_play',
        'has_ball_player_id',
        'player_action',
        'block_outcome',
        'rebounder_id',
        'shot_outcome',
        'turnover_steal',
    ]

    df_data = pd.DataFrame(columns=column_headers)

    start_play = True
    shooting_side_list = ['right', 'left']

    for i in range(num_sim):
        start_play, teams_list, shooting_side_list, player_action, block_outcome, rebounder_id, shot_outcome, turnover_steal, has_ball_player_id = sim_action(
            teams_list=teams_list,
            game_class=game_class,
            shooting_side_list=shooting_side_list,
            start_play=start_play,
        )

        df_data = update_data_df(
            df_data=df_data,
            start_play=start_play,
            has_ball_player_id=has_ball_player_id,
            player_action=player_action,
            block_outcome=block_outcome,
            rebounder_id=rebounder_id,
            shot_outcome=shot_outcome,
            turnover_steal=turnover_steal,
        )

    return df_data


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
