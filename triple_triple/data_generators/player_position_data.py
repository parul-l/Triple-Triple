import itertools
import json
import numpy as np
import pandas as pd


# Guided by:
# http://savvastjortjoglou.com/nba-play-by-play-movements.html

# January 11, 2016: MIA @ GSW
game_id = '0021500568'
tracking_file = '/Users/pl/Downloads/' + game_id + '.json'

def open_json(file_name):
    json_data = open(file_name).read()
    return json.loads(json_data)

data = open_json(tracking_file)    

headers_raw_pos_data = ["team_id",
                        "player_id",
                        "x_loc",
                        "y_loc",
                        "moment",
                        "period",
                        "game_clock",
                        "shot_clock"
                        ]
        
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

# create a data frame from the list
df_raw_position_data = pd.DataFrame(player_moments, columns = headers_raw_pos_data)

# create id dictionary
game_id_dict = {}

home_id = data['events'][0]['home']['teamid']
visitor_id = data['events'][0]['visitor']['teamid']

for item in data['events'][0]['home']['players']:
    game_id_dict[str(item['playerid'])] = [item['firstname'] + ' ' + item['lastname'], str(item['jersey']), str(home_id), item['position']]

for item in data['events'][0]['visitor']['players']:
    game_id_dict[str(item['playerid'])] = [item['firstname'] + ' ' + item['lastname'], 
    str(item['jersey']),str(visitor_id), item['position']]

# give the ball an id == -1    
game_id_dict.update({-1: ['ball', -1, -1, -1 ]})

# add player name and jersey number to dataframe
df_raw_position_data["player_name"] = df_raw_position_data.player_id.map(lambda x: game_id_dict[x][0])
df_raw_position_data["player_jersey"] = df_raw_position_data.player_id.map(lambda x: game_id_dict[x][1])

# drop duplicated rows. I don't know why the data is like this
df_raw_position_data = df_raw_position_data.drop_duplicates()

# Save file to make things easier
df_raw_position_data.to_csv('MIA_GSW_rawposition.csv')

##########################################
# Create a new DataFrame
# Just on times and all players positions
# Use this for the animations 
##########################################


# create df with headers = all players on roster
# MultiIndex format
# Each player name has (x, y) coord
coord_labels=['x_loc', 'y_loc']
headers_name = []   # each column is player name
headers_all_info = []        # each column is key+player name+jersey+team_id+position

player_ids = []

for key, value in game_id_dict.items():
    # combine the key, values in a list and flatten them
    # dataframe doesn't seem to work with headers with
    # different types as entries
    info = list(itertools.chain.from_iterable([[key], value]))
    headers_name.append(game_id_dict[key][0])
    headers_all_info.append(info)
    player_ids.append(key)
           
player_positions_all_times = []
period_positions =[]
game_clock_positions = []
len_events = len(data['events'])
for k in range(len_events):
    len_moments = len(data['events'][k]['moments'])
    for i in range(len_moments):
        moment = data['events'][k]['moments'][i][5]
        # Create empty list 
        # x2 for x and y coordinates
        # loc = [-10]* len(player_ids)*2 
        loc = np.empty(len(player_ids)*2)*np.nan
        for item in moment:
            # 2 x index to account for each player
            # corresponds to two slots
            idx = 2*player_ids.index(item[1])
            loc[idx] = item[2]
            loc[idx+1] = item[3]
        
        player_positions_all_times.append(loc)
        period_positions.append(moment[0][5])
        game_clock_positions.append(moment[0][6])    
   
# Create data frame of the data above
def get_positions():
    df_positions = pd.DataFrame(player_positions_all_times) 
    
    df_positions.columns = pd.MultiIndex.from_product([headers_name, coord_labels])
    
    # Insert period and game_clock
    # Don't like that it's at the end and its doubled. 
    # Re-indexing searches seem more complicated than needed.
    df_positions[('period','period')] = period_positions
    df_positions[('game_clock','game_clock')] = game_clock_positions

    return df_positions.drop_duplicates()

df_positions = get_positions()

# Save file 
df_positions.to_csv('MIA_GSW_positions.csv', index=False, tupleize_cols=False, float_format = '%.8f')

# Save game_id_dict
# Save the files as jsons but they become strings?
json.dump(game_id_dict, open('game_id_dict.json', 'wb'))
