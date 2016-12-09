import numpy as np
import triple_triple.prob_player_possessions as ppp

# TODO: create court image labeling the regions


def generate_back_court(shooting_side):
    if shooting_side == 'left':
        return [np.random.uniform(47, 94), np.random.uniform(0, 50)]
    elif shooting_side == 'right':
        return [np.random.uniform(0, 47), np.random.uniform(0, 50)]


def generate_mid_range(shooting_side):
    # break down the region in to 8 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate curved regions with triangles (for now)

    component = np.random.choice(np.arange(8), p=np.ones(8) / 8)

    if component == 0:
        if shooting_side == 'left':
            return [np.random.uniform(0, 14), np.random.uniform(3, 19)]
        elif shooting_side == 'right':
            return [np.random.uniform(80, 94), np.random.uniform(3, 19)]

    if component == 1:
        if shooting_side == 'left':
            return [np.random.uniform(0, 14), np.random.uniform(31, 47)]
        elif shooting_side == 'right':
            return [np.random.uniform(80, 94), np.random.uniform(31, 47)]

    if component == 2:
        if shooting_side == 'left':
            return [np.random.uniform(14, 19), np.random.uniform(5.64, 19)]
        elif shooting_side == 'right':
            return [np.random.uniform(75, 80), np.random.uniform(5.64, 19)]

    if component == 3:
        if shooting_side == 'left':
            return [np.random.uniform(14, 19), np.random.uniform(31, 44.36)]
        elif shooting_side == 'right':
            return [np.random.uniform(75, 80), np.random.uniform(31, 44.36)]

    if component == 4:
        # approximate with triangle
        # see below for formula http://math.stackexchange.com/questions/18686/uniform-randomoint-in-triangle
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([14, 3])
            b = np.array([19, 5.64])
            c = np.array([14, 5.64])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        elif shooting_side == 'right':
            a = np.array([80, 3])
            b = np.array([80, 5.64])
            c = np.array([75, 5.64])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 5:
        # approximate with triangle
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([14, 47])
            b = np.array([19, 44.36])
            c = np.array([14, 44.36])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        elif shooting_side == 'right':
            a = np.array([80, 47])
            b = np.array([80, 44.36])
            c = np.array([75, 44.36])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 6:
        # complicated region
        # approximate outer part with triangle (very crude)
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        # r = np.sqrt(np.random.uniform(0, 6))
        if shooting_side == 'left':
            a = np.array([19, 19])
            b = np.array([19, 5.64])
            c = np.array([29, 25])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        if shooting_side == 'right':
            a = np.array([65, 25])
            b = np.array([75, 5.64])
            c = np.array([75, 19])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 7:
        # complicated region
        # approximate with triangle (very crude)
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([19, 31])
            b = np.array([19, 44.36])
            c = np.array([29, 25])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        if shooting_side == 'right':
            a = np.array([65, 25])
            b = np.array([77, 44.36])
            c = np.array([75, 31])
            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c


def generate_key(shooting_side):
    # see below for formula
    # http://stats.stackexchange.com/questions/120527/how-to-generate-random-points-uniformly-distributed-in-a-circle

    # (x - 19)**2 + (y - 25)**2 <= 6**2
    r = np.sqrt(np.random.uniform(0, 6**2))

    if shooting_side == 'left':
        theta = (np.pi / 2) * np.random.uniform(-1, 1)
        return [19 + r * np.cos(theta), 25 + r * np.sin(theta)]

    elif shooting_side == 'right':
        theta = np.random.uniform(np.pi / 2, 3 * np.pi / 2)
        return [75 + r * np.cos(theta), 25 + r * np.sin(theta)]


def generate_out_of_bounds(shooting_side):
    # break down the region in to 3 components
    # randomly choose one of the components
    # generate coordinates in that component

    component = np.random.choice(np.arange(3), p=np.ones(3) / 3)

    if component == 0:
        if shooting_side == 'left':
            return [np.random.uniform(-2, 47), np.random.uniform(-2, 0)]
        elif shooting_side == 'right':
            return [np.random.uniform(47, 96), np.random.uniform(-2, 0)]

    elif component == 1:
        if shooting_side == 'left':
            return [np.random.uniform(-2, 0), np.random.uniform(0, 50)]
        elif shooting_side == 'right':
            return [np.random.uniform(94, 96), np.random.uniform(0, 50)]

    elif component == 2:
        if shooting_side == 'left':
            return [np.random.uniform(-2, 47), np.random.uniform(50, 52)]
        elif shooting_side == 'right':
            return [np.random.uniform(47, 96), np.random.uniform(50, 52)]


def generate_paint(shooting_side):
    if shooting_side == 'left':
        return [np.random.uniform(0, 19), np.random.uniform(19, 31)]
    elif shooting_side == 'right':
        return [np.random.uniform(75, 94), np.random.uniform(19, 31)]


def generate_perimeter(shooting_side):
    # break down the region in to 8 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate curved regions with triangles (for now)

    component = np.random.choice(np.arange(8), p=np.ones(8) / 8)

    if component == 0:
        if shooting_side == 'left':
            return [np.random.uniform(0, 19), np.random.uniform(0, 3)]
        elif shooting_side == 'right':
            return [np.random.uniform(75, 94), np.random.uniform(0, 3)]

    if component == 1:
        if shooting_side == 'left':
            return [np.random.uniform(0, 19), np.random.uniform(47, 50)]
        elif shooting_side == 'right':
            return [np.random.uniform(75, 94), np.random.uniform(47, 50)]

    if component == 2:
        # approximate with triangles
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([14, 3])
            b = np.array([19, 3])
            c = np.array([19, 5.64])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        elif shooting_side == 'right':
            a = np.array([75, 3])
            b = np.array([80, 3])
            c = np.array([80, 5.64])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 3:
        # approximate with triangles
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([14, 47])
            b = np.array([19, 47])
            c = np.array([19, 44.36])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        elif shooting_side == 'right':
            a = np.array([75, 47])
            b = np.array([80, 47])
            c = np.array([80, 44.36])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 4:
        if shooting_side == 'left':
            return [np.random.uniform(19, 29), np.random.uniform(0, 5.64)]

        elif shooting_side == 'right':
            return [np.random.uniform(65, 75), np.random.uniform(0, 5.64)]

    if component == 5:
        if shooting_side == 'left':
            return [np.random.uniform(19, 29), np.random.uniform(44.36, 50)]

        elif shooting_side == 'right':
            return [np.random.uniform(65, 75), np.random.uniform(44.36, 50)]

    if component == 6:
        # approximate with triangles
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([19, 5.64])
            b = np.array([29, 5.64])
            c = np.array([29, 25])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        elif shooting_side == 'right':
            a = np.array([75, 5.64])
            b = np.array([65, 5.64])
            c = np.array([65, 25])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 7:
        # approximate with triangles
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        if shooting_side == 'left':
            a = np.array([19, 44.36])
            b = np.array([29, 44.36])
            c = np.array([29, 25])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

        elif shooting_side == 'right':
            a = np.array([75, 44.36])
            b = np.array([65, 44.36])
            c = np.array([65, 25])

            return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
                r2 * np.sqrt(r1) * c

    if component == 8:
        if shooting_side == 'left':
            return [np.random.uniform(29, 47), np.random.uniform(0, 50)]

        elif shooting_side == 'right':
            return [np.random.uniform(47, 65), np.random.uniform(0, 50)]


def generate_rand_positions(pos_num, shooting_side):
    # back court
    if pos_num == 0:
        return generate_back_court(shooting_side)

    # mid-range
    elif pos_num == 1:
        return generate_mid_range(shooting_side)

    # key
    elif pos_num == 2:
        return generate_key(shooting_side)

    # out of bounds
    elif pos_num == 3:
        return generate_out_of_bounds(shooting_side)

    # paint
    elif pos_num == 4:
        return generate_paint(shooting_side)

    # perimeter
    elif pos_num == 5:
        return generate_perimeter(shooting_side)


def get_simulated_coord(player_sim_reg, shooting_side):
    coord = []
    for i in range(len(player_sim_reg)):
        coord.append(generate_rand_positions(player_sim_reg[i], shooting_side))
    return coord


def get_player_sim_reg(player_reg_prob_list, num_regions=6, num_sim=1000):
    return np.random.choice(
        a=np.arange(num_regions),
        p=player_reg_prob_list,
        size=num_sim
    )


def get_player_sim_poss(poss_per_sec, num_sim=1000):
    p = [1 - poss_per_sec, poss_per_sec]
    return np.random.choice(
        a=np.arange(2),
        p=p,
        size=num_sim
    )


def choose_next_region(start_region, prob_matrix, num_outcomes=6):

    return np.random.choice(
        a=np.arange(num_outcomes),
        p=prob_matrix[start_region, :],
        size=1
    ).flatten()


def get_simulated_play(
    player_sim_poss,
    player_sim_reg,
    prob_poss_type,
    pass_prob,
    shot_prob,
    assist_prob,
    turnover_prob,
    num_outcomes=4
):
    # determine indices where player has possession (list)
    idx_poss = np.argwhere(player_sim_poss == 1).flatten()
    # determine the region he is in at each index
    reg_poss = [player_sim_reg[item] for item in idx_poss]
    # determine array of possession outcomes
    poss_type = np.random.choice(
        a=np.arange(4),
        p=prob_poss_type,
        size=len(idx_poss)
    ).flatten()

    # determine result and next move at each possession
    # change the simulated region at i+1 to reflect possession probabilities
    # outcome array keeps track of possessions: pass, shot, assist, turnover
    outcome_array = np.zeros(num_outcomes)

    for i in range(len(idx_poss)):
        # get region at i
        reg_at_idx = reg_poss[i]
        # get possession type at i (pass, shot, assist, turnover)
        poss = poss_type[i]
        # determine region of next move
        # pass
        if poss == 0:
            player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, pass_prob)[0]
            outcome_array[0] += 1
        # shot
        if poss == 1:
            player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, shot_prob)[0]
            outcome_array[1] += 1
        # assist
        if poss == 2:
            player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, assist_prob)[0]

            # assists and shot increases
            outcome_array[1] += 1
            outcome_array[2] += 1
        # turnover
        if poss == 3:
            player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, turnover_prob)[0]
            outcome_array[3] += 1

    return player_sim_reg, outcome_array
