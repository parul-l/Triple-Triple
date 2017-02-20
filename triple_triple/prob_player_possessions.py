from collections import Counter
import numpy as np

# TODO: Change out of bounds to 0
# TODO: Change shooting probability to incorporate regions

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})


def get_reg_to_num(reg):
    if reg == 'back court':
        return 0
    if reg == 'mid-range':
        return 1
    if reg == 'key':
        return 2
    if reg == 'out of bounds':
        return 3
    if reg == 'paint':
        return 4
    if reg == 'perimeter':
        return 5


def court_region_from_number(num):
    if num == 0:
        return 'back court'
    if num == 1:
        return 'mid-range'
    if num == 2:
        return 'key'
    if num == 3:
        return 'out of bounds'
    if num == 4:
        return 'paint'
    if num == 5:
        return 'perimeter'


def get_poss_to_num(poss):
    if poss == 'pass':
        return 0
    if poss == 'shot':
        return 1
    if poss == 'turnover':
        return 2


def prob_from_list(counter_list, type_prob=None):
    count_dict = Counter(counter_list)
    total_sum = sum(count_dict.values())

    if type_prob is not None and None not in count_dict.keys():
        prob_list = np.zeros(len(count_dict))

        for outcome, count in count_dict.items():
            if type_prob == 'region':
                prob_list[get_reg_to_num(outcome)] = count

            elif type_prob == 'action':
                prob_list[get_poss_to_num(outcome)] = count

        return prob_list / float(sum(prob_list))

    else:
        prob_dict = {}
        for outcome, count in count_dict.items():
            prob_dict[outcome] = count / float(total_sum)

        return prob_dict


def get_region_prob_list(player_id_list, df_raw_position_region):
    region_prob = {}
    for player in player_id_list:
        region_list = df_raw_position_region.query('player_id==@player').region.values
        region_prob[player] = prob_from_list(counter_list=region_list, type_prob='region')

    return region_prob


def get_prob_count_matrix(count_matrix):
    return count_matrix / count_matrix.sum(axis=1)[:, None]


def update_region_prob_matrix(
    player_class,
    game_id,
    game_player_dict,
    df_raw_position_region,
    player_possession=False,
    team_on_offense=False,
    team_on_defense=False,
    half_court=True
):
    player_id = player_class.player_id
    team_id = player_class.team_id

    if player_possession is True:
        query_params = 'player_id==@player_id and closest_to_ball==True'
    # get times when player's team has possession
    elif team_on_offense is True:
        query_params = 'team_id==@team_id and closest_to_ball==True'
    # get times when player's team is on defense
    elif team_on_defense is True:
        query_params = 'team_id!=@team_id and closest_to_ball==True'
    else:
        query_params = 'player_id==@player_id'

    # get data for specific game
    df_game = df_raw_position_region.query('game_id==@game_id')

    if half_court is True:
        df_game = df_game.query('region != "back court"')

    # get times when player has possession
    keep_period = df_game.query(query_params).period.values
    keep_game_clock = df_game.query(query_params).game_clock.values

    # get regions for player with desired times
    reg_array = df_game.query('player_id==@player_id')[
        df_game.period.isin(keep_period) &
        df_game.game_clock.isin(keep_game_clock)
    ].region.values

    # create empty region_matrix
    region_matrix = np.zeros((6, 6))

    # use this to allow staying in a region
    # for i in range(len(reg_array) - 1):
    #     start_reg = get_reg_to_num(reg_array[i])
    #     end_reg = get_reg_to_num(reg_array[i + 1])
    #     region_matrix[start_reg, end_reg] += 1

    # determine where regions change
    idx_reg_change = np.where(reg_array[:-1] != reg_array[1:])[0]

    for idx in idx_reg_change:
        start_reg = get_reg_to_num(reg_array[idx])
        end_reg = get_reg_to_num(reg_array[idx + 1])

        region_matrix[start_reg, end_reg] += 1

    # update player_class
    player_class.region_prob_matrix = get_prob_count_matrix(region_matrix)


def update_possession_prob(
    player_class,
    df_possession,
    game_id=None
):
    if game_id is not None:
        df_possession = df_possession.query('game_id==@game_id')

    df_team_possession = df_possession\
        .query('team_id==@player_class.team_id and possession=="end"')
    df_player_possession = df_team_possession\
        .query('player_id==@player_class.player_id')

    # update player_class
    player_class.possession_prob = \
        len(df_player_possession) / float(len(df_team_possession))


def relative_player_possession_prob(players_offense_dict):
    raw_prob = []
    player_list = []

    for player, player_class in players_offense_dict.items():
        raw_prob.append(player_class.possession_prob)
        player_list.append(player)

    raw_prob = np.array(raw_prob)
    return player_list, raw_prob / raw_prob.sum()


def get_action_prob_matrix(player_class, df_possession):
    query_params = 'player_id==@player_class.player_id and possession=="end"'

    imp_columns = ['player_name', 'action', 'region', 'possession']
    df_player = df_possession.query(query_params)[imp_columns]

    # rows = region, columns = action [0, 1, 2] <--> [pass, shoot, turnover]
    possession_matrix = np.zeros((6, 3))

    for i in range(len(df_player)):
        end_reg = df_player.region.iloc[i]
        poss_num = get_poss_to_num(df_player.action.iloc[i])
        possession_matrix[get_reg_to_num(end_reg), poss_num] += 1

    player_class.action_prob_matrix = get_prob_count_matrix(possession_matrix)


def get_shooting_prob(player_class, df_game_stats):
    query_params = 'player_id==@player_class.player_id and \
                    (action=="shot" or action=="missed_shot")'
    df_player = df_game_stats.query(query_params)

    shot_prob = np.zeros(2)

    # get 2pt and 3pt prob
    for i in range(2, 4):
        df_specific_shot = df_player.query('other_note==@i')
        total_attempts = len(df_specific_shot)
        total_made = len(df_specific_shot.query('action=="shot"'))

        if total_attempts != 0:
            shot_prob[i - 2] = total_made / float(total_attempts)

    player_class.shooting_prob = shot_prob

########## OLD ONE ###################
###################################
# 
# def get_player_scoring_prob_region(known_player_possessions, type_shot):
#     # type_shot = 0, 2, or 3 <---> miss, 2pt, 3pt
# 
#     headers = [
#         'period',
#         'game_clock',
#         'start_region',
#         'end_region',
#         'possession',
#         'type_shot'
#     ]
#     df_shots = pd.DataFrame(known_player_possessions[0], columns=headers)
#     df_shots = df_shots.query('type_shot==@type_shot').reset_index()
# 
#     start = df_shots['start_region'].apply(get_reg_to_num)
# 
#     end = df_shots['end_region'].apply(get_reg_to_num)
# 
#     shot_matrix = np.zeros((6, 6))
#     # for each posession, count player shots
#     # for different regions on the court
#     # using only start (row) and end region (column) of possession
#     for i in range(len(start)):
#         shot_matrix[start[i], end[i]] += 1
# 
#     return shot_matrix
# 
# 
# def get_shot_type_prob(known_player_possessions):
#     total_shots = len(known_player_possessions[0])
#     num_miss = sum([1 for i in range(len(known_player_possessions[0])) if known_player_possessions[0][i][-1] == 0])
#     num_2pt = sum([1 for i in range(len(known_player_possessions[0])) if known_player_possessions[0][i][-1] == 2])
#     num_3pt = sum([1 for i in range(len(known_player_possessions[0])) if known_player_possessions[0][i][-1] == 3])
# 
#     try:
#         return np.array([num_miss, num_2pt, num_3pt]) / float(total_shots)
# 
#     except ZeroDivisionError:
#         pass
# 
# 
# def get_assist_prob(known_player_possessions, df_player_possession):
#     total_pass = len(df_player_possession[df_player_possession.type == 'pass'])
# 
#     try:
#         return len(known_player_possessions[1]) / float(total_pass)
# 
#     except ZeroDivisionError:
#         pass
# 
# 
# def get_player_region_prob(player_name, df_pos_dist_reg, num_regions=6):
#     df_player_region = list(df_pos_dist_reg[player_name].region)
#     # remove None values
#     df_player_region = [x for x in df_player_region if x is not None]
#     total_moments = len(df_player_region)
#     reg_prob_list = np.zeros(num_regions)
#     reg_prob_dict = {}
#     for region, count in Counter(df_player_region).items():
#         reg_prob_dict[region] = count / float(total_moments)
#         reg_prob_list[get_reg_to_num(region)] = count
# 
#     try:
#         return reg_prob_dict, reg_prob_list / float(total_moments)
# 
#     except ZeroDivisionError:
#         pass
# 
# 
# def get_reg_prob_no_backcourt(reg_prob_list):
#     total = reg_prob_list[1:].sum()
#     reg_prob_no_bc = reg_prob_list[1:] / total
#     # add 0 entry so that indicies follow reg_to_num
#     empty = np.array([0])
#     return np.concatenate((empty, reg_prob_no_bc))
# 
# 
# def get_prob_possession_type(df_player_possession, num_outcomes=3):
#     poss_type_to_num = {
#         'pass': 0,
#         'shot': 1,
#         'turnover': 2
#     }
#     poss_type_prob = np.zeros(num_outcomes)
#     for outcome, count in Counter(df_player_possession.type).items():
#         poss_type_prob[poss_type_to_num[outcome]] = count
# 
#     try:
#         return poss_type_prob / float(len(df_player_possession))
# 
#     except ZeroDivisionError:
#         pass
# 
# 
# def count_player_court_movement(df_pos_dist_reg, player_name, reg_to_num):
#     df_player = df_pos_dist_reg[df_pos_dist_reg[player_name].region.notnull()]
#     player_array = df_player[player_name].region.values
# 
#     # convert regions to numbers
#     for i in range(len(player_array)):
#         player_array[i] = reg_to_num[player_array[i]]
# 
#     movement_count_matrix = np.empty([6, 6])
#     for j in range(6):
#         reg_count = np.zeros(6)
#         for i in range(len(player_array) - 1):
#             if player_array[i] == j:
#                 reg_count[player_array[i + 1]] += 1
#         movement_count_matrix[j] = reg_count
# 
#     return movement_count_matrix
# 
# 
# def count_player_court_movement_poss(df_pos):
#     start = df_pos['start_region'].apply(get_reg_to_num)
# 
#     end = df_pos['end_region'].apply(get_reg_to_num)
# 
#     movement_matrix = np.zeros((6, 6))
#     # for each posession, count player movements
#     # for different regions on the court
#     # using only start (row) and end region (column) of possession
#     for i in range(len(start)):
#         movement_matrix[start[i], end[i]] += 1
#     return movement_matrix
# 
# 
# def cond_prob_per_region(count_matrix):
#     # given start region, probability of end region is
#     # each element divided by sum of its row
#     return count_matrix / count_matrix.sum(axis=1)[:, None]
# 
# 
# def poss_outcome_based_on_end_region(df_player_possession):
#     type_shot = df_player_possession['type'].apply(get_poss_to_num)
#     end = df_player_possession['end_region'].apply(get_reg_to_num)
# 
#     poss_matrix = np.zeros((6, 3))
# 
#     for i in range(len(end)):
#         poss_matrix[end[i], type_shot[i]] += 1
# 
#     return cond_prob_per_region(poss_matrix)
# 
# def get_possession_per_second(df_box_score, player_name):
#     total_min = df_box_score.query('PLAYER_NAME == @player_name')['MIN']\
#         .iloc[0].minute
#     total_sec = df_box_score.query('PLAYER_NAME == @player_name')['MIN']\
#         .iloc[0].second + total_min * 60
#     touches = df_box_score.query('PLAYER_NAME == @player_name')['TCHS'].iloc[0]
# 
#     try:
#         return touches / float(total_sec)
# 
#     except ZeroDivisionError:
#         pass
# 
# 
# def count_outcome_per_region(play_list, reg_to_num):
#     outcome_matrix = np.zeros((6, 6))
#     # create a matrix with outcome count
#     # row = start region
#     # column = end region
#     for item in play_list:
#         outcome_matrix[reg_to_num[item[2]], reg_to_num[item[3]]] += 1
#     return outcome_matrix
# 
# 
# def get_cond_prob_poss(known_player_possessions, play_pass, reg_to_num):
#     pass_not_assist_matrix = count_outcome_per_region(play_pass, reg_to_num)
# 
#     # shots = known_player_possessions[0]
#     shots_matrix = count_outcome_per_region(known_player_possessions[0], reg_to_num)
# 
#     # assists = known_player_possessions[1]
#     assist_matrix = count_outcome_per_region(known_player_possessions[1], reg_to_num)
# 
#     # turnovers = known_player_possessions[2]
#     turnover_matrix = count_outcome_per_region(known_player_possessions[2], reg_to_num)
# 
#     # cond probabilities
#     pass_not_assist_prob = pass_not_assist_matrix / pass_not_assist_matrix.sum(axis=1)[:, None]
#     shot_prob = shots_matrix / shots_matrix.sum(axis=1)[:, None]
#     assist_prob = assist_matrix / assist_matrix.sum(axis=1)[:, None]
#     turnover_prob = turnover_matrix / turnover_matrix.sum(axis=1)[:, None]
# 
#     # print reg_to_num
#     # print 'Row = start region, '
#     # print 'Column = end region'
# 
#     return pass_not_assist_prob, shot_prob, assist_prob, turnover_prob
# 
# 
# def get_player_outcome_prob_matrix_list(
#     df_pos_dist_reg,
#     player_name,
#     df_player_possession,
#     known_player_possessions,
#     play_pass,
#     reg_to_num
# ):
#     # this matrix is prob of movement regardless if player has possession
#     movement_matrix = count_player_court_movement(df_pos_dist_reg, player_name, reg_to_num)
#     # prob of going from back court to key is (0, 2) entry
#     movement_prob_matrix = cond_prob_per_region(movement_matrix)
# 
#     # shot per region raw count
#     miss_shots_matrix = get_player_scoring_prob_region(known_player_possessions, 0)
#     _2pt_shots_matrix = get_player_scoring_prob_region(known_player_possessions, 2)
#     _3pt_shots_matrix = get_player_scoring_prob_region(known_player_possessions, 3)
# 
#     # shot per region_probabilities
#     miss_shots_prob_matrix = cond_prob_per_region(miss_shots_matrix)
#     _2pt_shots_prob_matrix = cond_prob_per_region(_2pt_shots_matrix)
#     _3pt_shots_prob_matrix = cond_prob_per_region(_3pt_shots_matrix)
# 
#     # matrices of outcome conditional probabilities
#     # (0, 2) in pass_not_assist_prob gives prob of passing from backcourt to key
#     pass_not_assist_prob_matrix, shot_prob_matrix, assist_prob_matrix, turnover_prob_matrix = get_cond_prob_poss(
#         known_player_possessions, play_pass, reg_to_num)
# 
#     return [
#         movement_prob_matrix,
#         miss_shots_prob_matrix,
#         _2pt_shots_prob_matrix,
#         _3pt_shots_prob_matrix,
#         pass_not_assist_prob_matrix,
#         shot_prob_matrix,
#         assist_prob_matrix,
#         turnover_prob_matrix
#     ]
