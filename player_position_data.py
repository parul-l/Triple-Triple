import itertools
import json
import numpy as np
import pandas as pd
import copy

# Mostly following 
# http://savvastjortjoglou.com/nba-play-by-play-movements.html

# January 11, 2016: MIA @ GSW

tracking_file = "/Users/pl/Downloads/0021500568.json"

def open_json(file_name):
    json_data = open(file_name).read()
    return json.loads(json_data)

data = open_json(tracking_file)    

headers = ["team_id",
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
players_that_played = []
player_ids = []

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
df = pd.DataFrame(player_moments, columns = headers)

# create id dictionary
id_dict = {}

home_id = data['events'][0]['home']['teamid']
visitor_id = data['events'][0]['visitor']['teamid']


for item in data['events'][0]['home']['players']:
    id_dict[item['playerid']] = [item['firstname'] + ' ' + item['lastname'], 
                                item['jersey'], home_id, item['position']]

for item in data['events'][0]['visitor']['players']:
    id_dict[item['playerid']] = [item['firstname'] + ' ' + item['lastname'], 
                                item['jersey'],visitor_id, item['position']]

# give the ball an id == -1    
id_dict.update({-1: ['ball', -1, -1, -1 ]})

# add player name and jersey number to dataframe
df["player_name"] = df.player_id.map(lambda x: id_dict[x][0])
df["player_jersey"] = df.player_id.map(lambda x: id_dict[x][1])

# drop duplicated rows. I don't know why the data is like this
df = df.drop_duplicates()

#####################
# Create a new DataFrame
# Just on times and all players positions
# Use this for the animations 
#####################


# create df with headers = all players on roster
headers_pos = []        # append all info
headers_pos_name = []   # append only name
player_ids = []

for key, value in id_dict.items():
    # combine the key, values in a list and flatten them
    # dataframe doesn't seem to work with headers with
    # different types as entries
    info = list(itertools.chain.from_iterable([[key], value]))
    headers_pos_name.append(id_dict[key][0])
    headers_pos.append(info)
    player_ids.append(key)

headers_pos.insert(0, 'period')
headers_pos.insert(1, 'game_clock')

headers_pos_name.insert(0, 'period')
headers_pos_name.insert(1, 'game_clock')              


player_positions_all_times = []
len_events = len(data['events'])
for k in range(len_events):
    len_moments = len(data['events'][k]['moments'])
    for i in range(len_moments):
        moment = data['events'][k]['moments'][i][5]
        # Create empty list 
        loc = [(-10,-10)]* len(player_ids) 
        for item in moment:
            idx = player_ids.index(item[1])
            loc[idx] = (item[2], item[3])                
                
        # Combine and flatten lists
        new_list = [moment[0][5],  # period
                    moment[0][6]]  # game_clock 
        for x in loc:
            new_list.append(x)                                        
            player_positions_all_times.append(new_list)    
   
# Create data frame of the data above
def get_positions():
    df_positions = pd.DataFrame(player_positions_all_times, columns = headers_pos_name)          
    return df_positions.drop_duplicates()

df_positions = get_positions()
