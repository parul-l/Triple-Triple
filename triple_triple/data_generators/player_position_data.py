import json
import numpy as np
import pandas as pd
import os

from triple_triple.config import DATASETS_DIR


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
                #player_moments.append(item[:8])         

    headers_raw_pos_data = ['team_id',
                            'player_id',
                            'x_loc',
                            'y_loc',
                            'moment',   # height/radius of ball
                            'period',
                            'game_clock',
                            'shot_clock']
                            
    df_raw_position_data = pd.DataFrame(player_moments, columns=headers_raw_pos_data)                        
                            
    # add player name and jersey number to dataframe
    df_raw_position_data['player_name'] = df_raw_position_data.player_id.map(lambda x:  game_id_dict[str(x)][0])
    df_raw_position_data['player_jersey'] = df_raw_position_data.player_id.map(lambda x:    game_id_dict[str(x)][1])
    
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
    period =[]
    game_clock = []
    shot_clock = []
    ball_height = []
    len_events = len(data['events'])
    for k in range(len_events):
        len_moments = len(data['events'][k]['moments'])
        for i in range(len_moments):
            moment = data['events'][k]['moments'][i]
            # create empty list (*2 for x and y coordinates)
            loc = np.empty(len(player_ids)*2)*np.nan
            for item in moment[5]:
                # 2* index to account for each player
                # corresponding to two slots
                idx = 2*player_ids.index(str(item[1]))
                loc[idx] = item[2]
                loc[idx+1] = item[3]
            
            player_positions_all_times.append(loc)
            period.append(moment[0])
            game_clock.append(moment[2])    
            shot_clock.append(moment[3])
            ball_height.append(moment[5][0][4])

    df_positions = pd.DataFrame(player_positions_all_times) 
    df_positions.columns = pd.MultiIndex.from_product([headers_name, coord_labels])

    # insert period, game_clock, shot_clock, ball height/radius
    # don't like that it's at the end and its doubled. 
    # re-indexing searches seem more complicated than needed.
    df_positions['period'] = period
    df_positions['game_clock'] = game_clock
    df_positions['shot_clock'] = shot_clock
    df_positions['ball_height'] = ball_height 
            
    return df_positions.drop_duplicates()               
            
if __name__=='__main__':
    # January 11, 2016: MIA @ GSW
    game_id = '0021500568'
    tracking_file = '/Users/pl/Downloads/' + game_id + '.json'  
    
    data = open_json(tracking_file)
    game_id_dict = get_game_id_dict(data)
    df_raw_position_data = get_raw_position_data_df(data, game_id_dict)
    df_positions = get_player_positions_df(data,game_id_dict)
    
    # save files
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_rawposition.csv')     
    df_raw_position_data.to_csv(filepath)   
    
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_positions.csv')     
    df_positions.to_csv(filepath, index=False, tupleize_cols=False, float_format = '%.8f')
    
    # save game_id_dict
    # save the files as jsons but they become strings?
    filepath = os.path.join(DATASETS_DIR, 'game_id_dict.json')
    json.dump(game_id_dict, open(filepath, 'wb'))
