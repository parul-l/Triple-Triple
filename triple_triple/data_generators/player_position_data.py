import json
import numpy as np
import pandas as pd

from datetime import datetime


def open_json(file_name):
    json_data = open(file_name).read()
    return json.loads(json_data)


def get_game_info(data):
    game_info_dict = {
        'game_id': data['gameid'],
        'game_date': datetime.strptime(data['gamedate'], '%Y-%m-%d'),
        'hometeam_id': data['events'][0]['home']['teamid'],
        'visitorteam_id': data['events'][0]['visitor']['teamid'],
        'hometeam': data['events'][0]['home']['name'],
        'visitorteam': data['events'][0]['visitor']['name']
    }

    return game_info_dict


def get_game_player_dict(data):
    game_player_dict = {}

    hometeam_id = data['events'][0]['home']['teamid']
    visitorteam_id = data['events'][0]['visitor']['teamid']

    for item in data['events'][0]['home']['players']:
        game_player_dict[str(item['playerid'])] = [
            item['firstname'] + ' ' + item['lastname'],
            str(item['jersey']),
            str(hometeam_id),
            item['position']
        ]

    for item in data['events'][0]['visitor']['players']:
        game_player_dict[str(item['playerid'])] = [
            item['firstname'] + ' ' + item['lastname'],
            str(item['jersey']),
            str(visitorteam_id), item['position']
        ]

    # give the ball an id == -1
    game_player_dict['-1'] = ['ball', -1, -1, -1]

    return game_player_dict


def game_time_remaining_sec(period, game_clock):
    return (5 - period) * game_clock


def dist_two_points(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def closest_player_to_ball_array(dist_array):
    min_idxs = np.where(dist_array[1:] == dist_array[1:].min())
    closest_to_ball = [False] * 11
    for idx in min_idxs[0]:
        closest_to_ball[idx + 1] = True
    return closest_to_ball


def get_raw_position_data_df(data, game_player_dict, game_info_dict):
    len_events = len(data['events'])
    player_moments = []

    # create a list that contains info for each moment
    for m in range(1, len_events):
        event_moment = data['events'][m]['moments']
        len_moment = len(event_moment)
        for i in range(len_moment):
            # add basic_game_data
            additional_info = [
                game_info_dict['game_id'],          # game_id
                game_info_dict['game_date'],        # game_date
                event_moment[i][0],                 # period
                event_moment[i][2],                 # game_clock
                game_time_remaining_sec(
                    period=event_moment[i][0], game_clock=event_moment[i][2]), # game_time remaining in sec
                event_moment[i][3]                  # shot_clock
            ]

            # get dist_to_ball if it exists
            location_list = event_moment[i][5]

            if len(location_list) == 11:
                ball_x = location_list[0][2]
                ball_y = location_list[0][3]

                dist_to_ball = np.array([dist_two_points(ball_x, ball_y, item[2], item[3]) for item in location_list])

                closest_to_ball = closest_player_to_ball_array(dist_array=dist_to_ball)

            else:
                dist_to_ball = [None] * len(location_list)
                closest_to_ball = [None] * len(location_list)

            # add additional info, player_ball_dist, closest_to_ball to each moment
            [player_moments.append(
                additional_info +
                location_list[j] +
                [dist_to_ball[j]] +
                [closest_to_ball[j]]
            ) for j in range(len(location_list))]

    headers_raw_pos_data = [
        'game_id',
        'game_date',
        'period',
        'game_clock',
        'game_time_remain',
        'shot_clock',
        'team_id',
        'player_id',
        'x_loc',
        'y_loc',
        'moment',           # height/radius of ball
        'dist_to_ball',     # distance to ball
        'closest_to_ball'   # closest_to_ball if ball in play
    ]

    df_raw_position_data = pd.DataFrame(
        player_moments, columns=headers_raw_pos_data
    )

    # add player_name to dataframe
    df_raw_position_data['player_name'] = df_raw_position_data.player_id.map(
        lambda x: game_player_dict[str(x)][0]
    )

    # add jersey_number to dataframe
    df_raw_position_data['player_jersey'] = df_raw_position_data.player_id.map(
        lambda x: game_player_dict[str(x)][1]
    )

    return df_raw_position_data.drop_duplicates()

###################################################################
# create a new dataframe with every player's position at all times
# use this for the animations
###################################################################

# 
# def get_player_positions_df(data, game_id_dict):
# 
#     coord_labels = ['x_loc', 'y_loc']
#     headers_name = []
#     player_ids = []
# 
#     for key, value in game_id_dict.items():
#         headers_name.append(game_id_dict[key][0])
#         player_ids.append(key)
# 
#     player_positions_all_times = []
#     period = []
#     game_clock = []
#     shot_clock = []
#     ball_height = []
#     len_events = len(data['events'])
#     for k in range(len_events):
#         len_moments = len(data['events'][k]['moments'])
#         for i in range(len_moments):
#             moment = data['events'][k]['moments'][i]
#             # create empty list (*2 for x and y coordinates)
#             loc = np.empty(len(player_ids) * 2) * np.nan
#             for item in moment[5]:
#                 # 2* index to account for each player
#                 # corresponding to two slots
#                 idx = 2 * player_ids.index(str(item[1]))
#                 loc[idx] = item[2]
#                 loc[idx + 1] = item[3]
# 
#             player_positions_all_times.append(loc)
#             period.append(moment[0])
#             game_clock.append(moment[2])
#             shot_clock.append(moment[3])
#             ball_height.append(moment[5][0][4])
# 
#     df_positions = pd.DataFrame(player_positions_all_times)
#     df_positions.columns = pd.MultiIndex.from_product(
#         [headers_name, coord_labels]
#     )
# 
#     # insert period, game_clock, shot_clock, ball height/radius
#     # don't like that it's at the end and its doubled.
#     # re-indexing searches seem more complicated than needed.
#     df_positions['period'] = period
#     df_positions['game_clock'] = game_clock
#     df_positions['shot_clock'] = shot_clock
#     df_positions['ball_height'] = ball_height
# 
#     return df_positions.drop_duplicates()

###################################################################
# create a new dataframe with every player's position and distance
# from the ball at all times
# use this for the player_passing_habits
###################################################################


def get_closest_to_ball_df(dataframe):
    df_pos_x_loc = dataframe.iloc[:, dataframe
                                  .columns.get_level_values(1) == 'x_loc']
    df_pos_y_loc = dataframe.iloc[:, dataframe
                                  .columns.get_level_values(1) == 'y_loc']

    dist_x = (df_pos_x_loc.values.T - dataframe['ball']['x_loc'].values)**2
    dist_y = (df_pos_y_loc.values.T - dataframe['ball']['y_loc'].values)**2

    dist_to_ball_matrix = np.sqrt(dist_x + dist_y)

    # get column headers = player list
    # (Note: df_positions.columns.levels[0] doesn't preserve the order of the
    # columns)
    player_list = map(lambda x: x[0], df_pos_x_loc)

    # append distances to df_positions
    # there must be a better way to do this
    for i in range(len(player_list)):
        dataframe[player_list[i], 'dist'] = dist_to_ball_matrix[i]

    # remove ball column to get player relative distances
    df_positions_dist = dataframe\
        .sort_index(axis=1)\
        .drop('ball', level=0, axis=1)

    # find and remove ball column to get player relative distances
    # transpose so players are columns
    ball_idx = player_list.index('ball')
    dist_to_ball_matrix_no_ball = np.delete(
        dist_to_ball_matrix, (ball_idx), axis=0).T

    # sort to get lowest two distances
    # np.argpartition(matrix, 2 lowest, rows) gives an array of order
    # for max values, write -2, I think

    idx_sorted = np.argpartition(dist_to_ball_matrix_no_ball, 2, axis=1)
    dist_matrix_sorted = np.partition(dist_to_ball_matrix_no_ball, 2, axis=1)

    # [:,[0, 1, 2]] say, gives all rows and columns 0, 1, and 2
    idx_min = idx_sorted[:, 0]
    idx_second_min = idx_sorted[:, 1]

    min_values = dist_matrix_sorted[:, 0]
    second_min_values = dist_matrix_sorted[:, 1]

    # collect closest and second closest player to ball
    closest_player = []
    second_closest_player = []
    for i in range(len(idx_min)):
        closest_player.append(player_list[idx_min[i]])
        second_closest_player.append(player_list[idx_second_min[i]])

    # add back ball info
    df_positions_dist[('ball', 'x_loc')] = dataframe['ball']['x_loc']
    df_positions_dist[('ball', 'y_loc')] = dataframe['ball']['y_loc']

    # add closest player info to dataframe
    df_positions_dist['min_dist'] = min_values
    df_positions_dist['closest_player'] = closest_player

    df_positions_dist['second_min_dist'] = second_min_values
    df_positions_dist['second_closest_player'] = second_closest_player

    # reorder columns so ball is with players
    cols = df_positions_dist.columns.tolist()
    cols_reorder = cols[:78] + [('ball', 'x_loc')] + [('ball', 'y_loc')] \
        + cols[78:82] + cols[84:]

    df_positions_dist = df_positions_dist[cols_reorder]

    return df_positions_dist


def get_df_pos_trunc(df_pos_dist, has_ball_dist=2):
    return df_pos_dist[df_pos_dist.min_dist.values < has_ball_dist].reset_index()
