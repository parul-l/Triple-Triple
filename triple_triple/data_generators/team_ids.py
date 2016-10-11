import json
import os
import requests

from triple_triple.config import DATASETS_DIR


HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/45.0.2454.101 Safari/537.36'),
    'referer': 'http://stats.nba.com/player/'
}
          
def get_data(base_url, params):
    response = requests.get(base_url, params=params, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)

def get_team_ids(data):
    team_ids = {}
    team_ids_rev = {}

    for item in team_data['resultSets'][0]['rowSet']:
        team_ids[item[0]] = item[1]
        team_ids_rev[item[1]] = item[0]
    
    return team_ids, team_ids_rev    
                  
                        
##################
##################

if __name__ == '__main__':
    
    base_url = 'http://stats.nba.com/stats/leaguedashteamstats'

    # all these parameters appear to be necessary
    params = {
        'Conference':'',
        'DateFrom':'',
        'DateTo':'',
        'Division':'',
        'GameScope':'',
        'GameSegment':'',
        'LastNGames':'0',
        'LeagueID':'00',    
        'Location':'',            
        'MeasureType':'Base',
        'Month':'0',
        'OpponentTeamID':'0',
        'Outcome':'',         
        'PORound':'0',
        'PaceAdjust':'N',
        'PerMode':'PerGame',
        'Period':'0',
        'PlayerExperience':'',
        'PlayerPosition':'',
        'PlusMinus':'N',
        'Rank':'N',
        'Season':'2015-16',
        'SeasonSegment':'',
        'SeasonType':'Regular Season', 
        'ShotClockRange':'',
        'StarterBench':'',   
        'TeamID':'0',
        'VsConference':'',
        'VsDivision':'',
    }
          
    team_data = get_data(base_url, params)
    team_ids, team_ids_rev = get_team_ids(team_data)

    # Save the files as jsons (they become strings when opened)
    json_file = open(os.path.join(DATASETS_DIR, 'team_ids.json'), 'wb')
    json.dump(team_ids, json_file)
