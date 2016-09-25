############################################
############################################
# From NBA STATS! This takes too long! (approx. 20 min)
# See below for scraping from basketball-reference.com
###########################################
###########################################     
import json
import requests

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' 
                          'AppleWebKit/537.36 (KHTML, like Gecko)' 
                          'Chrome/51.0.2704.103 Safari/537.36'),
           'referer':     'http://stats.nba.com/player/'
          }

end_year='2016-17'
start_year='2016-17'
league_id = '00'
player_id = '201939'

base_url = 'http://stats.nba.com/stats/commonplayerinfo'
params = {'GraphEndSeason': end_year,
          'GraphStartSeason': start_year,
          'GraphStat': 'PTS',
          'LeagueID': league_id,
          'MeasureType':'Base',
          'PerMode':'PerGame',
          'PlayerID': player_id,
          'SeasonType':'Regular Season',
          'SeasonType': 'Playoffs'
          }
          
def get_data(base_url):
    response = requests.get(base_url, params = params, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)

def player_bio_nba_df():

    player_bio_info = []
    bad_keys = []

    for key in player_ids.keys():
        try:
            player_id = str(key)
                
            params = {'GraphEndSeason': end_year,
                      'GraphStartSeason': start_year,
                      'GraphStat': 'PTS',
                      'LeagueID': league_id,
                      'MeasureType':'Base',
                      'PerMode':'PerGame',
                      'PlayerID': player_id,
                      'SeasonType':'Regular Season',
                      'SeasonType': 'Playoffs'
                    }
                    
            player_data = get_data(base_url)
            
            player_bio_info.append(
                    [player_data['resultSets'][0]['rowSet'][0][0],  # id
                     player_data['resultSets'][0]['rowSet'][0][4],  # name
                     player_data['resultSets'][0]['rowSet'][0][22], # from
                     player_data['resultSets'][0]['rowSet'][0][23], # to
                     player_data['resultSets'][0]['rowSet'][0][14], # position
                     player_data['resultSets'][0]['rowSet'][0][10], # height
                     player_data['resultSets'][0]['rowSet'][0][11], # weight
                     player_data['resultSets'][0]['rowSet'][0][6],  # bday
                    ])
        except:
            bad_keys.append(key)  
                                                       
    bio_headers = ['Player_ID',
                   'Player_Name',
                   'From',
                   'To',
                   'Position',
                   'Height',
                   'Weight',
                   'Birthdate'                
                   ]
                                                  
    return pd.DataFrame(player_bio_info, columns=bio_headers)                

df_player_bio = player_bio_nba_df()
# Save file
df_player_bio.to_csv('player_bio_info.csv')

############################################
############################################
# From Web Scraping: A lot shorter but possibly not 100% accurate
###########################################
###########################################   

from bs4 import BeautifulSoup
from datetime import datetime, date, time
import numpy as np
import pandas as pd
#from player_ids import remove_unwanted_char
from player_ids import player_ids
from player_ids import player_ids_rev
import requests
import string

def parse_data(url):
    response = requests.get(url)

    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    tables = soup.findChildren('table')
    my_table = tables[0]
    return my_table.findChildren(['tr'])

def remove_unwanted_char(some_string):
    new_string = some_string.replace('.', '')
    new_string = new_string.replace('*', '')
    return new_string       

def player_bio_scraped_df():
    player_bio_info = []
    bad_rows = []       # non-player rows
    bad_character = []  # letters with no one 

    # iterate through alphabet to get all players and bios
    # subtract 1 from 'from' and 'to' to match nba.com
    for c in string.ascii_lowercase:
        url = "http://www.basketball-reference.com/players/" + c + "/"
        try:
            rows = parse_data(url)
            for row in rows:
                name_cell = row.findChildren('th')
                cells = row.findChildren('td')
                try:
                    temp_list= [remove_unwanted_char(name_cell[0].text), # name
                                int(cells[0].text)-1,                # from 
                                int(cells[1].text)-1,                # to
                                cells[2].text,                       # position
                                cells[3].text,                       # height  
                                int(cells[4].text),                   # weight
                                datetime.strptime(cells[5].text, '%B %d, %Y')] # birthday
                    player_bio_info.append(temp_list)
                except:
                    bad_rows.append(row.text)
        except:
            bad_character.append(c)
        
    headers = ["Player Name",
                "From",
                "To",
                "Position",
                "Height",
                "Weight",
                "Birthdate"
              ]        

    df_player_bio = pd.DataFrame(player_bio_info, columns=headers) 
        
    # match players from player_ids to player_bio_info        
    current_year = 2016
    id_index =np.zeros(len(player_bio_info), int)
    unidentify_index0=[]
    unidentify_index_current_yr = []
    unidentify_index = []
    for key, value in player_ids.iteritems():
        try:
            idx=df_player_bio.loc[
                                (df_player_bio['Player Name']==value[0]) &
                                (df_player_bio['From']==value[1])
                                ].index
            
            # unique player names and years
            if len(idx)==1:
                id_index[idx] = key
            
            # players not found   
            elif len(idx)==0:
                idx0= df_player_bio.loc[(df_player_bio['Player Name']==value[0])].index
                # unique players based just on name, not years
                if len(idx0)==1:
                    id_index[idx0] = key
                            
                elif value[1]==current_year:
                    # key, name, from, to, position, height, weight, bday
                    unidentify_index_current_yr.append([key, value[0], value[1], 
                                                    value[2],'NaN', 'NaN', 0, 0])
                else:   
                    # key, name, from, to, position, height, weight, bday
                    unidentify_index0.append([key, value[0], value[1], value[2],
                                            'NaN', 'NaN', 0, 0])                                                                                     
            else:
                # multiple index players
                unidentify_index.append((idx, key, value))
        except:
            print key, value 

    # Add player_ids to DataFrame
    df_player_bio.insert(0, 'Player_ID', id_index)

    # Add players starting in 2016 that are not
    # on basketball-reference. 
    # Sloppy way of doing it
    headers_current_yr = ["Player_ID",
                          "Player Name",
                          "From",
                          "To",
                          "Position",
                          "Height",
                          "Weight",
                          "Birthdate"
                          ]

    df_current_year = pd.DataFrame(unidentify_index_current_yr, 
                                    columns=headers_current_yr )
    return df_player_bio.append(df_current_year,ignore_index =True) 

if __name__=='__main__':
    df_player_bio = player_bio_scraped_df()
    # Save file
    df_player_bio.to_csv('player_bio_info.csv')

# Update From/To years in datafram so it matches with NBA stats website.
