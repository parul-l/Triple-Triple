from collections import Counter
import numpy as np

# TODO: Define the dictionary get_reg_to_num and make sure nothing breaks!
# TODO: Change shooting probability to incorporate regions
# TODO: Determine average length of a possession (in seconds?)

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})


get_reg_to_num = {
    'paint': 0,
    'mid-range': 1,
    'key': 2,
    'perimeter': 3,
    'back_court': 4,
    'out_of_bounds': 5
}


def get_reg_to_num(reg):
    if reg == 'paint':
        return 0
    if reg == 'mid_range':
        return 1
    if reg == 'key':
        return 2
    if reg == 'perimeter':
        return 3
    if reg == 'back_court':
        return 4
    if reg == 'out_of_bounds':
        return 5


def court_region_from_number(num):
    if num == 0:
        return 'paint'
    if num == 1:
        return 'mid_range'
    if num == 2:
        return 'key'
    if num == 3:
        return 'perimeter'
    if num == 4:
        return 'back_court'
    if num == 5:
        return 'out_of_bounds'


def get_action_to_num(action):
    if action == 'pass':
        return 0
    if action == 'shot' or action == 'missed_shot':
        return 1
    if action == 'turnover':
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
                prob_list[get_action_to_num(outcome)] = count

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


def update_region_freq_matrix(
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
        df_game = df_game.query('region != "back_court"')

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

    # update player_class freq count
    player_class.region_freq_matrix = region_matrix


def update_region_prob_matrix(player_class):
    # prob matrix
    player_class.region_prob_matrix = get_prob_count_matrix(player_class.region_freq_matrix)


def update_possession_prob(
    player_class,
    df_possession,
    game_id=None
):
    if game_id is not None:
        df_possession = df_possession.query('game_id==@game_id')

    df_team_possession = df_possession\
        .query('team_id==@player_class.team_id and possession_end')
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


def get_action_freq_matrix(player_class, df_possession):
    query_params = 'player_id==@player_class.player_id and possession_end'

    imp_columns = ['player_name', 'action', 'region', 'possession_start', 'possession_end']
    df_player = df_possession.query(query_params)[imp_columns]

    # rows = region, columns = action [0, 1, 2] <--> [pass, shoot, turnover]
    possession_matrix = np.zeros((6, 3))

    for i in range(len(df_player)):
        end_reg = df_player.region.iloc[i]
        poss_num = get_action_to_num(df_player.action.iloc[i])
        possession_matrix[get_reg_to_num(end_reg), poss_num] += 1

    # update player_class freq count
    player_class.action_freq_matrix = possession_matrix


def get_action_prob_matrix(player_class):
    # action prob
    player_class.action_prob_matrix = get_prob_count_matrix(player_class.action_freq_matrix)


def get_shooting_freq(player_class, df_game_stats):
    query_params = 'player_id==@player_class.player_id and \
                    (action=="shot" or action=="missed_shot")'
    df_player = df_game_stats.query(query_params)

    shot_freq = []

    # get 2pt and 3pt prob
    for i in range(2, 4):
        df_specific_shot = df_player.query('other_note==@i')
        total_attempts = len(df_specific_shot)
        total_made = len(df_specific_shot.query('action=="shot"'))

        shot_freq.append((total_made, float(total_attempts)))
        # shot_prob[i - 2] = total_made / float(total_attempts)

    player_class.shooting_freq = shot_freq


def get_shooting_prob(player_class):
    shot_freq = player_class.shooting_freq
    # if total_attempts != 0:
    #     shot_prob[0] = player_class.shooting_freq
    shot_prob = [x[0] / x[1] if x[1] != 0 else 0 for x in shot_freq]
    player_class.shooting_prob = shot_prob


def get_action_freq_array(player_class, df_possession, action):
    df_player = df_possession.query('player_id==@player_class.player_id')

    action_count = Counter(df_player.query('action==@action').region.values)

    action_freq_array = np.zeros(6)
    for region, count in action_count.items():
        action_freq_array[get_reg_to_num(region)] = count

    return action_freq_array


def get_regional_shooting_freq(player_class, df_possession):
    made_shot_array = get_action_freq_array(
        player_class=player_class,
        df_possession=df_possession,
        action="shot")
    missed_shot_array = get_action_freq_array(
        player_class=player_class,
        df_possession=df_possession,
        action="missed_shot")

    player_class.region_shooting_freq = {
        'made_shot': made_shot_array,
        'missed_shot': missed_shot_array
    }


def get_regional_shooting_prob(player_class):
    made_shot_array = \
        player_class.region_shooting_freq['made_shot']
    missed_shot_array = \
        player_class.region_shooting_freq['missed_shot']
    total_shots = made_shot_array + missed_shot_array

    # find prob and replace nan with zero
    player_class.region_shooting_prob = np.nan_to_num(
        made_shot_array / total_shots
    )
