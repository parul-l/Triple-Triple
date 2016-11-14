import json
import math
import numpy as np
import pandas as pd


# Guided by:
# http://savvastjortjoglou.com/nba-play-by-play-movements.html


def open_json(file_name):
    json_data = open(file_name).read()
    return json.loads(json_data)


def get_game_id_dict(data):
    game_id_dict = {}

    home_id = data['events'][0]['home']['teamid']
    visitor_id = data['events'][0]['visitor']['teamid']

    for item in data['events'][0]['home']['players']:
        game_id_dict[str(item['playerid'])] = [
            item['firstname'] + ' ' + item['lastname'],
            str(item['jersey']), str(home_id),
            item['position']
        ]

    for item in data['events'][0]['visitor']['players']:
        game_id_dict[str(item['playerid'])] = [
            item['firstname'] + ' ' + item['lastname'],
            str(item['jersey']),
            str(visitor_id), item['position']
        ]

    # give the ball an id == -1
    game_id_dict['-1'] = ['ball', -1, -1, -1]

    return game_id_dict


def get_raw_position_data_df(data, game_id_dict):
    len_events = len(data['events'])
    player_moments = []

    # create a list that contains all the header info for each moment
    for m in range(1, len_events):
        len_moment = len(data['events'][m]['moments'])
        for i in range(len_moment):
            for item in data['events'][m]['moments'][i][5]:
                item.append(data['events'][m]['moments'][i][0])
                item.append(data['events'][m]['moments'][i][2])
                item.append(data['events'][m]['moments'][i][3])
                player_moments.append(item)
                # player_moments.append(item[:8])

    headers_raw_pos_data = [
        'team_id',
        'player_id',
        'x_loc',
        'y_loc',
        'moment',   # height/radius of ball
        'period',
        'game_clock',
        'shot_clock'
    ]

    df_raw_position_data = pd.DataFrame(
        player_moments, columns=headers_raw_pos_data
    )

    # add player name and jersey number to dataframe
    df_raw_position_data['player_name'] = df_raw_position_data.player_id.map(
        lambda x: game_id_dict[str(x)][0]
    )
    df_raw_position_data['player_jersey'] = df_raw_position_data.player_id.map(
        lambda x: game_id_dict[str(x)][1]
    )

    return df_raw_position_data.drop_duplicates()

###################################################################
# create a new dataframe with every player's position at all times
# use this for the animations
###################################################################


def get_player_positions_df(data, game_id_dict):

    coord_labels = ['x_loc', 'y_loc']
    headers_name = []
    player_ids = []

    for key, value in game_id_dict.items():
        headers_name.append(game_id_dict[key][0])
        player_ids.append(key)

    player_positions_all_times = []
    period = []
    game_clock = []
    shot_clock = []
    ball_height = []
    len_events = len(data['events'])
    for k in range(len_events):
        len_moments = len(data['events'][k]['moments'])
        for i in range(len_moments):
            moment = data['events'][k]['moments'][i]
            # create empty list (*2 for x and y coordinates)
            loc = np.empty(len(player_ids) * 2) * np.nan
            for item in moment[5]:
                # 2* index to account for each player
                # corresponding to two slots
                idx = 2 * player_ids.index(str(item[1]))
                loc[idx] = item[2]
                loc[idx + 1] = item[3]

            player_positions_all_times.append(loc)
            period.append(moment[0])
            game_clock.append(moment[2])
            shot_clock.append(moment[3])
            ball_height.append(moment[5][0][4])

    df_positions = pd.DataFrame(player_positions_all_times)
    df_positions.columns = pd.MultiIndex.from_product(
        [headers_name, coord_labels]
    )

    # insert period, game_clock, shot_clock, ball height/radius
    # don't like that it's at the end and its doubled.
    # re-indexing searches seem more complicated than needed.
    df_positions['period'] = period
    df_positions['game_clock'] = game_clock
    df_positions['shot_clock'] = shot_clock
    df_positions['ball_height'] = ball_height

    return df_positions.drop_duplicates()

###################################################################
# create a new dataframe with every player's position and distance
# from the ball at all times
# use this for the player_passing_habits
###################################################################


def dist_two_points(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2)


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
    # import pdb; pdb.set_trace()
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
