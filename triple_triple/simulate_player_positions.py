import numpy as np

# TODO: create court image labeling the regions
# Use midpoint of the region as the simulated coordinate
# TODO: check right side boundary points. 75 should be 80?

def generate_back_court(shooting_side):
    if shooting_side == 'left':
        return [70.5, 25]
    elif shooting_side == 'right':
        return [23.5, 25]


def generate_mid_range(shooting_side):
    # break down the region in to 3 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate with rectangles and triangles

    component = np.random.choice(np.arange(3), p=np.ones(3) / 3)
    if component == 0:
        if shooting_side == 'left':
            return [9.5, 11]
        elif shooting_side == 'right':
            return [84.5, 11]

    if component == 1:
        if shooting_side == 'left':
            return [9.5, 39]
        elif shooting_side == 'right':
            return [84.5, 39]

    if component == 2:
        if shooting_side == 'left':
            return [27.5, 25]
        elif shooting_side == 'right':
            return [67, 25]


def generate_key(shooting_side):
    # approximate with rectangle

    if shooting_side == 'left':
        return [22, 25]
    elif shooting_side == 'right':
        return [72, 25]


def generate_paint(shooting_side):
    if shooting_side == 'left':
        return [9.5, 25]
    elif shooting_side == 'right':
        return [84.5, 25]


def generate_out_of_bounds(shooting_side):
    # use behind the rim
    if shooting_side == 'left':
        return [-2, 25]

    elif shooting_side == 'right':
        return [96, 25]


def generate_perimeter(shooting_side):
    # break down the region in to 4 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate with rectangles and triangles

    component = np.random.choice(np.arange(4), p=np.ones(4) / 4)
    if component == 0:
        if shooting_side == 'left':
            return [7, 1.5]
        elif shooting_side == 'right':
            return [89, 1.5]

    if component == 1:
        if shooting_side == 'left':
            return [7, 48.5]
        elif shooting_side == 'right':
            return [89, 48.5]

    if component == 2:
        # centroid of triangle (19, 3), (47, 0), (47, 25)
        if shooting_side == 'left':
            return [37.67, 9.33]
        # centroid of triangle (75, 3), (47, 0), (47, 25)
        elif shooting_side == 'right':
            return [56.33, 9.33]

    if component == 3:
        # centroid of triangle (19, 47), (47, 25), (47, 50)
        if shooting_side == 'left':
            return [37.67, 40.67]
        # centroid of triangle (75, 47), (47, 25), (47, 50)
        elif shooting_side == 'right':
            return [56.33, 40.67]


def get_simulated_coord(player_sim_reg, shooting_side):
    coord = []
    for i in range(len(player_sim_reg)):
        coord.append(generate_rand_positions(player_sim_reg[i], shooting_side))
    return coord


def get_player_sim_reg(cond_prob_movement, num_sim, num_regions=6):
    # use 'out of bounds = 3' as the first region
    sim_reg = np.array([3])
    # determine remaining region based on conditional probabilities of movement
    for i in range(1, num_sim):
        next_region = np.random.choice(
            a=np.arange(num_regions),
            p=cond_prob_movement[sim_reg[i - 1], :],
            size=1
        )
        sim_reg = np.append(sim_reg, next_region)

    return sim_reg


def get_player_sim_poss(poss_per_sec, num_sim):
    p = [1 - poss_per_sec, poss_per_sec]
    return np.random.choice(
        a=np.arange(2),
        p=p,
        size=num_sim
    )


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



################################# OLD #################################

# 
# 
# def generate_back_court(shooting_side):
#     if shooting_side == 'left':
#         return [np.random.uniform(47, 94), np.random.uniform(0, 50)]
#     elif shooting_side == 'right':
#         return [np.random.uniform(0, 47), np.random.uniform(0, 50)]
# 
# 
# def generate_mid_range(shooting_side):
#     # break down the region in to 8 components
#     # randomly choose one of the components
#     # generate coordinates in that component
#     # approximate curved regions with triangles (for now)
# 
#     component = np.random.choice(np.arange(8), p=np.ones(8) / 8)
# 
#     if component == 0:
#         if shooting_side == 'left':
#             return [np.random.uniform(0, 14), np.random.uniform(3, 19)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(80, 94), np.random.uniform(3, 19)]
# 
#     if component == 1:
#         if shooting_side == 'left':
#             return [np.random.uniform(0, 14), np.random.uniform(31, 47)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(80, 94), np.random.uniform(31, 47)]
# 
#     if component == 2:
#         if shooting_side == 'left':
#             return [np.random.uniform(14, 19), np.random.uniform(5.64, 19)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(75, 80), np.random.uniform(5.64, 19)]
# 
#     if component == 3:
#         if shooting_side == 'left':
#             return [np.random.uniform(14, 19), np.random.uniform(31, 44.36)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(75, 80), np.random.uniform(31, 44.36)]
# 
#     if component == 4:
#         # approximate with triangle
#         # see below for formula http://math.stackexchange.com/questions/18686/uniform-randomoint-in-triangle
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([14, 3])
#             b = np.array([19, 5.64])
#             c = np.array([14, 5.64])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         elif shooting_side == 'right':
#             a = np.array([80, 3])
#             b = np.array([80, 5.64])
#             c = np.array([75, 5.64])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 5:
#         # approximate with triangle
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([14, 47])
#             b = np.array([19, 44.36])
#             c = np.array([14, 44.36])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         elif shooting_side == 'right':
#             a = np.array([80, 47])
#             b = np.array([80, 44.36])
#             c = np.array([75, 44.36])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 6:
#         # complicated region
#         # approximate outer part with triangle (very crude)
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         # r = np.sqrt(np.random.uniform(0, 6))
#         if shooting_side == 'left':
#             a = np.array([19, 19])
#             b = np.array([19, 5.64])
#             c = np.array([29, 25])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         if shooting_side == 'right':
#             a = np.array([65, 25])
#             b = np.array([75, 5.64])
#             c = np.array([75, 19])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 7:
#         # complicated region
#         # approximate with triangle (very crude)
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([19, 31])
#             b = np.array([19, 44.36])
#             c = np.array([29, 25])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         if shooting_side == 'right':
#             a = np.array([65, 25])
#             b = np.array([77, 44.36])
#             c = np.array([75, 31])
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
# 
# def generate_key(shooting_side):
#     # see below for formula
#     # http://stats.stackexchange.com/questions/120527/how-to-generate-random-points-uniformly-distributed-in-a-circle
# 
#     # (x - 19)**2 + (y - 25)**2 <= 6**2
#     r = np.sqrt(np.random.uniform(0, 6**2))
# 
#     if shooting_side == 'left':
#         theta = (np.pi / 2) * np.random.uniform(-1, 1)
#         return [19 + r * np.cos(theta), 25 + r * np.sin(theta)]
# 
#     elif shooting_side == 'right':
#         theta = np.random.uniform(np.pi / 2, 3 * np.pi / 2)
#         return [75 + r * np.cos(theta), 25 + r * np.sin(theta)]
# 
# 
# def generate_out_of_bounds(shooting_side):
#     # break down the region in to 3 components
#     # randomly choose one of the components
#     # generate coordinates in that component
# 
#     component = np.random.choice(np.arange(3), p=np.ones(3) / 3)
# 
#     if component == 0:
#         if shooting_side == 'left':
#             return [np.random.uniform(-2, 47), np.random.uniform(-2, 0)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(47, 96), np.random.uniform(-2, 0)]
# 
#     elif component == 1:
#         if shooting_side == 'left':
#             return [np.random.uniform(-2, 0), np.random.uniform(0, 50)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(94, 96), np.random.uniform(0, 50)]
# 
#     elif component == 2:
#         if shooting_side == 'left':
#             return [np.random.uniform(-2, 47), np.random.uniform(50, 52)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(47, 96), np.random.uniform(50, 52)]
# 
# 
# def generate_paint(shooting_side):
#     if shooting_side == 'left':
#         return [np.random.uniform(0, 19), np.random.uniform(19, 31)]
#     elif shooting_side == 'right':
#         return [np.random.uniform(75, 94), np.random.uniform(19, 31)]
# 
# 
# def generate_perimeter(shooting_side):
#     # break down the region in to 8 components
#     # randomly choose one of the components
#     # generate coordinates in that component
#     # approximate curved regions with triangles (for now)
# 
#     component = np.random.choice(np.arange(8), p=np.ones(8) / 8)
# 
#     if component == 0:
#         if shooting_side == 'left':
#             return [np.random.uniform(0, 19), np.random.uniform(0, 3)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(75, 94), np.random.uniform(0, 3)]
# 
#     if component == 1:
#         if shooting_side == 'left':
#             return [np.random.uniform(0, 19), np.random.uniform(47, 50)]
#         elif shooting_side == 'right':
#             return [np.random.uniform(75, 94), np.random.uniform(47, 50)]
# 
#     if component == 2:
#         # approximate with triangles
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([14, 3])
#             b = np.array([19, 3])
#             c = np.array([19, 5.64])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         elif shooting_side == 'right':
#             a = np.array([75, 3])
#             b = np.array([80, 3])
#             c = np.array([80, 5.64])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 3:
#         # approximate with triangles
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([14, 47])
#             b = np.array([19, 47])
#             c = np.array([19, 44.36])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         elif shooting_side == 'right':
#             a = np.array([75, 47])
#             b = np.array([80, 47])
#             c = np.array([80, 44.36])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 4:
#         if shooting_side == 'left':
#             return [np.random.uniform(19, 29), np.random.uniform(0, 5.64)]
# 
#         elif shooting_side == 'right':
#             return [np.random.uniform(65, 75), np.random.uniform(0, 5.64)]
# 
#     if component == 5:
#         if shooting_side == 'left':
#             return [np.random.uniform(19, 29), np.random.uniform(44.36, 50)]
# 
#         elif shooting_side == 'right':
#             return [np.random.uniform(65, 75), np.random.uniform(44.36, 50)]
# 
#     if component == 6:
#         # approximate with triangles
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([19, 5.64])
#             b = np.array([29, 5.64])
#             c = np.array([29, 25])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         elif shooting_side == 'right':
#             a = np.array([75, 5.64])
#             b = np.array([65, 5.64])
#             c = np.array([65, 25])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 7:
#         # approximate with triangles
#         r1 = np.random.uniform(0, 1)
#         r2 = np.random.uniform(0, 1)
# 
#         if shooting_side == 'left':
#             a = np.array([19, 44.36])
#             b = np.array([29, 44.36])
#             c = np.array([29, 25])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#         elif shooting_side == 'right':
#             a = np.array([75, 44.36])
#             b = np.array([65, 44.36])
#             c = np.array([65, 25])
# 
#             return (1 - np.sqrt(r1)) * a + np.sqrt(r1) * (1 - r2) * b +\
#                 r2 * np.sqrt(r1) * c
# 
#     if component == 8:
#         if shooting_side == 'left':
#             return [np.random.uniform(29, 47), np.random.uniform(0, 50)]
# 
#         elif shooting_side == 'right':
#             return [np.random.uniform(47, 65), np.random.uniform(0, 50)]

# 
# def generate_rand_positions(pos_num, shooting_side):
#     # back court
#     if pos_num == 0:
#         return generate_back_court(shooting_side)
# 
#     # mid-range
#     elif pos_num == 1:
#         return generate_mid_range(shooting_side)
# 
#     # key
#     elif pos_num == 2:
#         return generate_key(shooting_side)
# 
#     # out of bounds
#     elif pos_num == 3:
#         return generate_out_of_bounds(shooting_side)
# 
#     # paint
#     elif pos_num == 4:
#         return generate_paint(shooting_side)
# 
#     # perimeter
#     elif pos_num == 5:
#         return generate_perimeter(shooting_side)
# 
# 
# def get_simulated_coord(player_sim_reg, shooting_side):
#     coord = []
#     for i in range(len(player_sim_reg)):
#         coord.append(generate_rand_positions(player_sim_reg[i], shooting_side))
#     return coord
# 
# 
# def get_player_sim_reg(player_reg_prob_list, cond_prob_movement, num_sim, num_regions=6):
#     # determine first region using reg_prob_list
#     sim_reg = np.random.choice(
#         a=np.arange(num_regions),
#         p=player_reg_prob_list,
#         size=1
#     )
#     # determine remaining region based on conditional probabilities of movement
#     for i in range(1, num_sim):
#         next_region = np.random.choice(
#             a=np.arange(num_regions),
#             p=cond_prob_movement[sim_reg[i - 1], :],
#             size=1
#         )
#         sim_reg = np.append(sim_reg, next_region)
# 
#     return sim_reg
# 
# 
# def get_player_sim_poss(poss_per_sec, num_sim):
#     p = [1 - poss_per_sec, poss_per_sec]
#     return np.random.choice(
#         a=np.arange(2),
#         p=p,
#         size=num_sim
#     )
# 
# 
# 
# # simulate plays for one player
# def get_simulated_play(
#     player_sim_poss,
#     player_sim_reg_temp,
#     prob_poss_type,
#     prob_shot_type,
#     prob_assist,
#     pass_prob_matrix,
#     assist_prob_matrix,
#     turnover_prob_matrix,
#     miss_shots_prob_matrix,
#     _2pt_shots_prob_matrix,
#     _3pt_shots_prob_matrix,
#     num_outcomes=3
# ):
#     # determine indices where player has possession (list)
#     idx_poss = np.argwhere(player_sim_poss == 1).flatten()
#     # determine the region he is in at each index
#     reg_poss = [player_sim_reg_temp[item] for item in idx_poss]
#     # determine array of possession outcomes (pass, shoot, turnover)
#     poss_type = np.random.choice(
#         a=np.arange(3),
#         p=prob_poss_type,
#         size=len(idx_poss)
#     ).flatten()
# 
#     # determine result and next move at each possession
#     # change the simulated region at i+1 to reflect possession probabilities
#     # outcome array keeps track of possessions:
#     # [pass, shot_miss, shot_2pt, shot_3pt, assist, turnover]
#     outcome_array = np.zeros(6)
#     points_count = 0
# 
#     for i in range(len(idx_poss)):
#         # get region at i
#         reg_at_idx = reg_poss[i]
#         # get possession type at i (pass, shot, assist, turnover)
#         poss = poss_type[i]
#         # determine region of next move
#         # pass
#         if poss == 0:
#             # determine if pass is assist or not
#             # 0 = no assist, 1 = assist
#             pass_type = np.random.choice(
#                 a=np.arange(2),
#                 p=[1 - prob_assist, prob_assist],
#                 size=1
#             ).flatten()
#             # no assist
#             if pass_type == 0:
#                 player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, pass_prob_matrix)[0]
#                 outcome_array[0] += 1
# 
#             # pass is assist
#             if pass_type == 1:
#                 player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, assist_prob_matrix)[0]
#                 outcome_array[4] += 1
#                 points_count += 2   # assuming 2 point field goal
# 
#         # shot
#         if poss == 1:
#             # determine type of shot (0 = miss, 1 = 2pt, 2 = 3pt)
#             shot_type = np.random.choice(
#                 a=np.arange(3),
#                 p=prob_shot_type,
#                 size=1
#             ).flatten()
# 
#             # miss
#             if shot_type == 0:
#                 player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, miss_shots_prob_matrix)[0]
#                 outcome_array[1] += 1
#             # 2 pt
#             elif shot_type == 1:
#                 player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, _2pt_shots_prob_matrix)[0]
#                 outcome_array[2] += 1
#                 points_count += 2
#             # 3 pt
#             elif shot_type == 2:
#                 player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, _3pt_shots_prob_matrix)[0]
#                 outcome_array[3] += 1
#                 points_count += 3
# 
#         # turnover
#         if poss == 2:
#             player_sim_poss[idx_poss[i] + 1] = choose_next_region(reg_at_idx, turnover_prob_matrix)[0]
#             outcome_array[5] += 1
# 
#     return player_sim_poss, outcome_array, points_count
# 
# 
# ######################################################
# # Functions for multi-player simulation
# ######################################################
# 
# def get_simulated_regions_dict(player_list, all_players_poss_prob_dict,
#                                all_players_outcome_prob_matrix_dict):
# 
#     # all_players_poss_prob_dict[0] = reg_prob_list_no_bc
#     simulated_regions_dict = {}
#     for i in range(len(player_list)):
#         simulated_regions_dict[player_list[i]] = get_player_sim_reg(all_players_poss_prob_dict[player_list[i]][0], all_players_outcome_prob_matrix_dict[player_list[i]][0], num_sim=5000, num_regions=6)
#     return simulated_regions_dict
# 
# 
# def get_simulated_region_coord_dict(player_list, simulated_regions_dict):
#     simulated_region_coord_dict = {}
#     for i in range(len(player_list)):
#         simulated_region_coord_dict[player_list[i]] = get_simulated_coord(simulated_regions_dict[player_list[i]], 'left')
#     return simulated_region_coord_dict
# 
# 
# 
# 
# def dist_two_coord(x, y):
#     return np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
# 
# 
# def get_closest_player_to_ball_region(
#     idx,
#     player_with_ball,
#     player_list,
#     simulated_region_coord_dict
# ):
#     num_players = len(player_list)
#     player_ball_coord = simulated_region_coord_dict[player_list[player_with_ball]][idx]
# 
#     dist_array = np.empty(num_players) * np.nan
#     for i in range(num_players):
#         if not i == player_with_ball:
#             dist_array[i] = dist_two_coord(player_ball_coord, simulated_region_coord_dict[player_list[i]][idx])
# 
#     return np.nanargmin(dist_array)
# 
# 
# def backcourt_violation(region1, region2):
#     if region2 == 0 and region1 != 0:
#         return True
# 
# # USING CLASSES
# 
# 
# def pick_player_with_ball(players_on_court):
#     # use probability of possession to determine likelihood of possession
#     all_poss_per_sec = np.array([players_on_court[i].prob_lists[5] for i in range(len(players_on_court))])
# 
#     prob_poss = all_poss_per_sec / float(all_poss_per_sec.sum())
#     return np.random.choice(
#         a=np.arange(len(players_on_court)),
#         p=prob_poss,
#         size=1
#     ).flatten()[0]
# 
# 
# def choose_next_region(start_region, prob_matrix, num_outcomes=6):
# 
#     return np.random.choice(
#         a=np.arange(num_outcomes),
#         p=prob_matrix[start_region, :],
#         size=1
#     ).flatten()[0]
# 
# 
# def if_pass(player_with_ball, players_on_court):
#     # choose player to pass to
#     # pass to yourself means you move with the ball
# 
#     # find index of player in players_on_court
#     idx = players_on_court.index(player_with_ball)
# 
#     # assign probabilities of passing
#     # assume pass to oneself is 0.5 and remaining divided equally
#     # TODO: Fix these especially when adding shot clock parameters
# 
#     p = np.full(len(players_on_court), 0.5 / (len(players_on_court) - 1))
#     p[idx] = 0.5
# 
#     new_possession = np.random.choice(
#         a=np.arange(len(players_on_court)),
#         p=p,
#         size=1
#     ).flatten()[0]
# 
#     # update players' possession status
#     player_with_ball.possession = False
#     players_on_court[new_possession].possession = True
# 
#     # update players' region using movement_prob_matrix
#     for i in range(len(players_on_court)):
#         reg = players_on_court[i].court_region
# 
#         new_region = choose_next_region(
#             reg,
#             players_on_court[i].prob_matrices[0],
#             num_outcomes=6
#         )
# 
#         players_on_court[i].court_region = new_region
# 
# 
# def if_shoot(player_with_ball, players_on_court):
#     # find index of player in players_on_court
#     idx = players_on_court.index(player_with_ball)
#     
#     # determine type of shot (0 = miss, 1 = 2pt, 2 = 3pt)
#     shot_type = np.random.choice(
#         a=np.arange(3),
#         p=player_with_ball.prob_lists[3],
#         size=1
#     ).flatten()[0]
# 
#     # update players' region using movement_prob_matrix
#     for i in range(len(players_on_court)):
#         if i != idx:
#             # use movement_matrix for players without possession
#             movement_matrix = 0
#         else:
#             # use shooting_matrix for player with possession
#             movement_matrix = 5
# 
#         reg = players_on_court[i].court_region
#         new_region = choose_next_region(
#             reg,
#             players_on_court[i].prob_matrices[movement_matrix],
#             num_outcomes=6
#         )
#         players_on_court[i].court_region = new_region
# 
#     # update possession_status
#     player_with_ball.possession = False
# 
#     return shot_type
# 
# 
# def if_turnover(player_with_ball, players_on_court):
#     # update possession_status
#     player_with_ball.possession = False
# 
#     # update players' region using turnover_prob_matrix
#     for i in range(len(players_on_court)):
#         reg = players_on_court[i].court_region
# 
#         new_region = choose_next_region(
#             reg,
#             players_on_court[i].prob_matrices[7],
#             num_outcomes=6
#         )
# 
#         players_on_court[i].court_region = new_region
# 
# 
# def simulate_one_play(players_on_court):
#     # check who has possession of the ball
#     try:
#         idx_ball = [players_on_court[i].possession for i in range(len(players_on_court))].index(True)
#     except:
#         idx_ball = pick_player_with_ball(players_on_court)
# 
#     # determine outcome
#     poss_outcome = np.random.choice(
#         a=np.arange(3),
#         p=players_on_court[idx_ball].prob_lists[2],
#         size=1
#     ).flatten()[0]
# 
#     return idx_ball, poss_outcome
# 
# 
# 
# 
# 
# 
# 
#     
# def if_sim_pass(
#     player_with_ball,
#     player_list,
#     simulated_regions_dict,
#     simulated_region_coord_dict,
#     all_players_poss_prob_dict,
#     all_players_outcome_prob_matrix_dict,
#     points_count,
#     outcome_array,
#     player_possession_array,
#     poss_type_array,
#     play_stop,
#     idx
# ):
#     player_name = player_list[player_with_ball]
#     # determine if pass leads to assist
#     # 0 = no assist, 1 = assist
# 
#     pass_type = np.random.choice(
#         a=np.arange(2),
#         p=[1 - all_players_poss_prob_dict[player_name][4], all_players_poss_prob_dict[player_name][4]],
#         size=1
#     ).flatten()
# 
#     # not assist
#     if pass_type == 0:
#         pass_matrix = 4
#         poss_type_array[idx] = (0, 0)
#     # pass is assist
#     if pass_type == 1:
#         pass_matrix = 6
#         poss_type_array[idx] = (0, 1)
# 
#     next_player_ball_region = \
#         choose_next_region(
#             simulated_regions_dict[player_name][idx],
#             all_players_outcome_prob_matrix_dict[player_name][pass_matrix]
#         )[0]
# 
#     # find closest player to player with ball at idx = i+1
#     # this player is assumed to be the next player with the ball
#     player_with_ball = get_closest_player_to_ball_region(
#         idx + 1,
#         player_with_ball,
#         player_list,
#         simulated_region_coord_dict
#     )
# 
#     player_possession_array[idx + 1] = player_with_ball
#     simulated_regions_dict[player_list[player_with_ball]][idx + 1] = next_player_ball_region
#     # simulated_region_coord_dict[player_list[player_with_ball]] = generate_rand_positions(next_player_ball_region, 'left')
# 
# 
#     # check if there is a backcourt violation
#     # this case needs to not happen since we want a legit pass, not turnover
#     if backcourt_violation(
#         simulated_regions_dict[player_name][idx + 1], simulated_regions_dict[player_list[player_with_ball]][idx + 1]
#     ):
#        # stop the play and choose random for possession
#        poss_type_array[idx] = (0, -1)
#        play_stop += 1
#        player_with_ball = pick_player_with_ball(player_list)
# 
#     else:
#         # poss_outcome of new player is NOT a shot
#         if pass_type == 0:
#             outcome_array[0] += 1
# 
#         # poss_outcome of new player is a shot
#         if pass_type == 1:
#             poss_outcome = 1
#             choose_player_possession = False
#             choose_shot_type = False
#             outcome_array[4] += 1
# 
#             if next_player_ball_region == 0 or 5:
#                 shot_type = 2
#             else:
#                 shot_type = 1
# 
#             play_stop += 1
#             player_with_ball = pick_player_with_ball(player_list)
# 
#     # subtract an index so in next iteration, player_possession_array
#     # is accurate
#     idx -= 1
# 
#     return simulated_regions_dict, outcome_array, player_possession_array, play_stop, points_count, player_with_ball, poss_type_array
# 
# 
# def if_sim_shot(
#     player_with_ball,
#     player_list,
#     simulated_regions_dict,
#     all_players_poss_prob_dict,
#     all_players_outcome_prob_matrix_dict,
#     points_count,
#     outcome_array,
#     player_possession_array,
#     poss_type_array,
#     play_stop,
#     choose_shot_type,
#     idx
# ):
# 
#     player_name = player_list[player_with_ball]
#     player_possession_array[idx] = player_with_ball
# 
#     # determine type of shot (0 = miss, 1 = 2pt, 2 = 3pt)
#     if choose_shot_type is True:
# 
#         shot_type = np.random.choice(
#             a=np.arange(3),
#             p=all_players_poss_prob_dict[player_name][2],
#             size=1
#         ).flatten()
# 
#     # miss
#     if shot_type == 0:
#         simulated_regions_dict[player_name][idx + 1] = \
#             choose_next_region(
#                 simulated_regions_dict[player_name][idx],
#                 all_players_outcome_prob_matrix_dict[player_name][1])[0]
#         outcome_array[1] += 1
#         poss_type_array[idx] = (1, 0)
# 
#     # 2 pt
#     elif shot_type == 1:
#         simulated_regions_dict[player_name][idx + 1] = \
#             choose_next_region(
#                 simulated_regions_dict[player_name][idx],
#                 all_players_outcome_prob_matrix_dict[player_name][2])[0]
#         outcome_array[2] += 1
#         points_count += 2
#         poss_type_array[idx] = (1, 1)
# 
#     # 3 pt
#     elif shot_type == 2:
#         simulated_regions_dict[player_name][idx + 1] = \
#             choose_next_region(
#                 simulated_regions_dict[player_name][idx],
#                 all_players_outcome_prob_matrix_dict[player_name][3])[0]
#         outcome_array[3] += 1
#         points_count += 3
#         poss_type_array[idx] = (1, 2)
# 
#     play_stop += 1
#     player_with_ball = pick_player_with_ball(player_list)
#     choose_player_possession = True
# 
#     return outcome_array, player_possession_array, play_stop, points_count, player_with_ball, poss_type_array
# 
# 
# def if_sim_turnover(
#     player_with_ball,
#     player_list,
#     simulated_regions_dict,
#     all_players_outcome_prob_matrix_dict,
#     outcome_array,
#     player_possession_array,
#     poss_type_array,
#     play_stop,
#     idx
# ):
#     player_name = player_list[player_with_ball]
#     player_possession_array[idx] = player_with_ball
# 
#     simulated_regions_dict[player_name][idx + 1] = choose_next_region(
#         simulated_regions_dict[player_name][idx],
#         all_players_outcome_prob_matrix_dict[player_name][7]
#     )[0]
#     outcome_array[5] += 1
# 
#     poss_type_array[idx] = (2, -1)
#     play_stop += 1
#     player_with_ball = pick_player_with_ball(player_list)
#     choose_player_possession = True
# 
#     return outcome_array, player_possession_array, play_stop, player_with_ball, poss_type_array
# 
# # simulate play for multiple players on court
# 
# 
# def get_simulate_play_mult_players(
#     player_list,
#     simulated_regions_dict,
#     simulated_region_coord_dict,
#     all_players_poss_prob_dict,
#     all_players_outcome_prob_matrix_dict
# ):
#     num_sim = len(simulated_regions_dict[player_list[0]])
# 
#     # outcome array keeps track of possessions:
#     # [pass, shot_miss, shot_2pt, shot_3pt, assist, turnover]
#     outcome_array = np.zeros(6)
#     player_possession_array = np.full(num_sim, np.nan)
#     poss_type_array = np.full((num_sim, 2), np.nan)
#     points_count = 0
#     play_stop = 0
#     choose_player_possession = True
#     choose_shot_type = True
# 
#     # determine first player with ball
#     player_with_ball = pick_player_with_ball(player_list)
# 
#     # determine result and next move at each possession
#     # change the simulated region at i+1 to reflect possession probabilities
# 
#     for i in range(num_sim - 1):
#         player_possession_array[i] = player_with_ball
#         player_name = player_list[player_with_ball]
# 
#         if choose_player_possession is True:
#             # determine player_with_ball outcome probabilities:
#             player_poss_prob = all_players_poss_prob_dict[player_name][1]
#             # choose an outcome
#             poss_outcome = np.random.choice(
#                 a=np.arange(len(player_poss_prob)),
#                 p=player_poss_prob,
#                 size=1
#             ).flatten()
# 
#         # pass
#         if poss_outcome == 0:
#             # outcome of pass
#             simulated_regions_dict, outcome_array, player_possession_array, play_stop, points_count, player_with_ball, poss_type_array = if_sim_pass(
#                 player_with_ball=player_with_ball,
#                 player_list=player_list,
#                 simulated_regions_dict=simulated_regions_dict,
#                 simulated_region_coord_dict=simulated_region_coord_dict,
#                 all_players_poss_prob_dict=all_players_poss_prob_dict,
#                 all_players_outcome_prob_matrix_dict=all_players_outcome_prob_matrix_dict,
#                 points_count=points_count,
#                 outcome_array=outcome_array,
#                 player_possession_array=player_possession_array,
#                 poss_type_array=poss_type_array,
#                 play_stop=play_stop,
#                 idx=i
#             )
#         # shoot
#         elif poss_outcome == 1:
#             outcome_array, player_possession_array, play_stop, points_count, player_with_ball, poss_type_array = if_sim_shot(
#                 player_with_ball=player_with_ball,
#                 player_list=player_list,
#                 simulated_regions_dict=simulated_regions_dict,
#                 all_players_poss_prob_dict=all_players_poss_prob_dict,
#                 all_players_outcome_prob_matrix_dict=all_players_outcome_prob_matrix_dict,
#                 points_count=points_count,
#                 outcome_array=outcome_array,
#                 player_possession_array=player_possession_array,
#                 poss_type_array=poss_type_array,
#                 play_stop=play_stop,
#                 choose_shot_type=choose_shot_type,
#                 idx=i
#             )
#             choose_shot_type = True
# 
#         # turnover
#         elif poss_outcome == 2:
#             outcome_array, player_possession_array, play_stop, player_with_ball, poss_type_array = if_sim_turnover(
#                 player_with_ball=player_with_ball,
#                 player_list=player_list,
#                 simulated_regions_dict=simulated_regions_dict,
#                 all_players_outcome_prob_matrix_dict=all_players_outcome_prob_matrix_dict,
#                 outcome_array=outcome_array,
#                 player_possession_array=player_possession_array,
#                 poss_type_array=poss_type_array,
#                 play_stop=play_stop,
#                 idx=i
#             )
# 
#     return points_count, outcome_array, player_possession_array, poss_type_array, play_stop
