import json
import numpy as np
import pandas as pd

from datetime import datetime


def open_json(file_name):
    with open(file_name, 'r') as f:
        json_data = f.read()
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
        game_player_dict[item['playerid']] = [
            item['firstname'] + ' ' + item['lastname'],
            item['jersey'],
            hometeam_id,
            item['position']
        ]

    for item in data['events'][0]['visitor']['players']:
        game_player_dict[item['playerid']] = [
            item['firstname'] + ' ' + item['lastname'],
            item['jersey'],
            visitorteam_id, item['position']
        ]

    # give the ball an id == -1
    game_player_dict[-1] = ['ball', -1, -1, -1]

    return game_player_dict


def game_time_remaining_sec(period, game_clock):
    return (4 - period) * 720. + game_clock


def dist_two_points(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def closest_player_to_ball_array(dist_array):
    min_idxs = np.where(dist_array[1:] == dist_array[1:].min())
    closest_to_ball = [False] * 11
    for idx in min_idxs[0]:
        closest_to_ball[idx + 1] = True
    return closest_to_ball


def get_raw_position_data_df(data, game_player_dict, game_info_dict, has_ball_dist=2):
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

                # has_ball_dist_array = add_has_ball_dist_to_df(closest_player=closest_to_ball, dist_to_ball=dist_to_ball, has_ball_dist=has_ball_dist)

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
        'moment',               # height/radius of ball
        'dist_to_ball',         # distance to ball
        'closest_to_ball',      # closest_to_ball if ball in play
    ]

    df_raw_position_data = pd.DataFrame(
        player_moments, columns=headers_raw_pos_data
    )

    # add player_name to dataframe
    df_raw_position_data['player_name'] = df_raw_position_data.player_id.map(
        lambda x: game_player_dict[x][0]
    )

    # add jersey_number to dataframe
    df_raw_position_data['player_jersey'] = df_raw_position_data.player_id.map(
        lambda x: game_player_dict[x][1]
    )

    return df_raw_position_data.drop_duplicates().reset_index(drop=True)
