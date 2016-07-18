import requests
import json

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
           'referer': 'http://stats.nba.com/player/'
          }

current_season = '2015'

def get_data(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)
    
player_url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16"

data = get_data(player_url)

player_headers = [
    data['resultSets'][0]['headers'][0],    # Person_ID
    data['resultSets'][0]['headers'][1],    # Last, First
    data['resultSets'][0]['headers'][3],    # Roster Status
    data['resultSets'][0]['headers'][4],    # From Year
    data['resultSets'][0]['headers'][5],    # To Year
    data['resultSets'][0]['headers'][7],    # Team ID
    data['resultSets'][0]['headers'][9]     # Team_Name
]

player_info_all= {}
for i in range(len(data['resultSets'][0]['rowSet'])):    
    temp_dict = {}
    temp_dict[player_headers[0]] = data['resultSets'][0]['rowSet'][i][0]
    temp_dict[player_headers[1]] = data['resultSets'][0]['rowSet'][i][1]
    temp_dict[player_headers[2]] = data['resultSets'][0]['rowSet'][i][3]
    temp_dict[player_headers[3]] = data['resultSets'][0]['rowSet'][i][4]
    temp_dict[player_headers[4]] = data['resultSets'][0]['rowSet'][i][5]
    temp_dict[player_headers[5]] = data['resultSets'][0]['rowSet'][i][7]
    temp_dict[player_headers[6]] = data['resultSets'][0]['rowSet'][i][9]
    
    player_info_all[data['resultSets'][0]['rowSet'][i][0]] = temp_dict

player_info_current = []
for key in player_info_all:
    if player_info_all[key]['TO_YEAR']==current_season:
        player_info_current.append(player_info_all[key])

# Collect player stats

stats_headers = [
"SEASON"
"TEAM"
"PLAYER_AGE",
"GAMES_PLAYED",
"GAMES_STARTED",
"MIN",
"PTS"
"FGM",
"FGA",
"FG_PCT",
"FG3M",
"FG3A",
"FG3_PCT",
"FTM",
"FTA",
"FT_PCT",
"OREB",
"DREB",
"AST",
"STL",
"BLK",
"TO",
"FOULS",
]

player_keys = []
for key in player_info_all:
    player_keys.append(key)

# Want this data for i in range(len(player_keys)), but it was taking too long
player_stats = {}
for i in range(100): 
    key = player_keys[i]
    url = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=" + str(key)
    data = get_data(url)
    
    player_stats[key] = []
    for item in data['resultSets'][0]['rowSet']:
            
            player_stats[key].append(
            [{
            'Season':   item[1],     # Season 
            'Team':     item[4],     # Team
            'Age':      item[5],     # Age
            'GP':       item[6],     # GP
            'GS':       item[7],     # GS
            'MIN':      item[8],     # MIN
            'PTS':      item[26],    # PTS
            'FGM':      item[9],     # FGM
            'FGA':      item[10],    # FGA
            'FG_PCT':   item[11],    # FG_PCT
            'FG3M':     item[12],    # FG3M
            'FG3A':     item[13],    # FG3A
            'FG3_PCT':  item[14],    # FG3_PCT
            'FTM':      item[15],    # FTM
            'FTA':      item[16],    # FTA
            'FT_PCT':   item[17],    # FT_PCT
            'OREB':     item[18],    # OREB
            'DREB':     item[19],    # DREB
            'AST':      item[21],    # AST
            'STL':      item[22],    # STL
            'BLK':      item[23],    # BLK
            'TO':       item[24],    # TO
            'PF':       item[25],    # PF
            'SAL':      1000000,     # salary -> MADE UP RIGHT NOW
            # add player transaction 
            
            }])
        
# Determine a player's length of time in the league up to a given season
def time_in_league(key, year):
    no_teams_season = []   
    for i in range(len(player_stats[key])):
        if player_stats[key][i][0]['Season'] == year:
            all_years.append(i)
    return min(no_teams_season)

player_career_stats = {}
for i in range(len(player_info_current)):
    player_id = player_info_current[i]['PERSON_ID']
    
    url = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID="+ str(player_id)
    data = get_data(url)
    try:
        list_of_career_stats = data['resultSets'][1]['rowSet'][0]
        list_of_season_stats = data['resultSets'][0]['rowSet']  #list of lists
        
        player_career_stats[player_id] = [
        list_of_season_stats[len(list_of_season_stats) - 1][5], # Age
        list_of_career_stats[3],     # GP
        list_of_career_stats[4],     # GS
        list_of_career_stats[5],     # MIN
        list_of_career_stats[23],    # PTS
        list_of_career_stats[6],     # FGM
        list_of_career_stats[7],     # FGA
        list_of_career_stats[8],     # FG_PCT
        list_of_career_stats[9],     # FG3A
        list_of_career_stats[10],    # FG3M
        list_of_career_stats[11],    # FG3_PCT
        list_of_career_stats[12],    # FTM
        list_of_career_stats[13],    # FTA
        list_of_career_stats[14],    # FT_PCT
        list_of_career_stats[15],    # OREB
        list_of_career_stats[16],    # DREB
        list_of_career_stats[18],    # AST
        list_of_career_stats[19],    # STL
        list_of_career_stats[20],    # BLK
        list_of_career_stats[21],    # TO
        list_of_career_stats[22],    # PF
        # added player transaction below
        ]
    except:
        print player_id
    
# Add transanction results to player_career_stats
# Total: 22 elements in list

execfile('Transaction_Results.py')

for k in player_trans_affect:
    if k in player_career_stats:
        player_career_stats[k].append(player_trans_affect[k])
        
# Add player salaries to player_career_stats
# First: Match up player names to IDs. Some names are odd

execfile('Salary.py')

player_salary = {}
try:
    for key in player_salary_interm:
        for item in player_info_all:
            if item['DISPLAY_LAST_COMMA_FIRST'] == key:
                player_salary[(key, item['PERSON_ID'])] =   player_salary_interm[key]         

except:
    print key
# To get the players who were traded in 2015-16
# for k in player_career_stats:
#     if len(player_career_stats[k])==22:
#         print k, player_career_stats[k]                
