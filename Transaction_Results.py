import Player_Info
import Team_Info
import requests
import json
import datetime

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
           'referer': 'http://stats.nba.com/team/'
          }

def get_data(url, headers=HEADERS):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)
            
trans_url = "http://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json"

data = get_data(trans_url)

transaction_headers = ['PLAYER_ID',
                        'TEAM_ID',
                        'TRANSACTION_DATE',
                        'TRANSACTION_DESCRIPTION',
                        'TRANSACTION_TYPE',        
                        ] 

transaction_info = []
no_transactions = len(data['NBA_Player_Movement']['rows'])
for i in range(no_transactions):
    transaction_info.append([
    int(data['NBA_Player_Movement']['rows'][i]['PLAYER_ID']),
    int(data['NBA_Player_Movement']['rows'][i]['TEAM_ID']),
    datetime.datetime.strptime(data['NBA_Player_Movement']['rows'][i]['TRANSACTION_DATE'], "%Y-%m-%dT%H:%M:%S"),
    #data['NBA_Player_Movement']['rows'][i]['TRANSACTION_DATE'],
    data['NBA_Player_Movement']['rows'][i]['TRANSACTION_DESCRIPTION'],
    data['NBA_Player_Movement']['rows'][i]['Transaction_Type']
    ]
    ) 

season = "2015-16"
league_url="http://stats.nba.com/stats/leaguegamelog?Counter=1000&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season=2015-16&SeasonType=Regular+Season&Sorter=PTS"
team_data = get_data(league_url)

def team_success(team_id, date):
    wins_before_date = 0
    loss_before_date = 0
    wins_after_date = 0
    loss_after_date = 0
    
    no_games = len(team_data['resultSets'][0]['rowSet'])
    
    for i in range(no_games):
        if (team_data['resultSets'][0]['rowSet'][i][1] ==int(team_id) and 
        datetime.datetime.strptime(team_data['resultSets'][0]['rowSet'][i][5], "%Y-%m-%d") < date 
        and
        team_data['resultSets'][0]['rowSet'][i][7] == 'W'):
            
            wins_before_date +=1
            
        elif (team_data['resultSets'][0]['rowSet'][i][1] ==int(team_id) and 
        datetime.datetime.strptime(team_data['resultSets'][0]['rowSet'][i][5], "%Y-%m-%d") < date 
        and
        team_data['resultSets'][0]['rowSet'][i][7] == 'L'):
            
            loss_before_date +=1    
        
        elif (team_data['resultSets'][0]['rowSet'][i][1] ==int(team_id) and 
        datetime.datetime.strptime(team_data['resultSets'][0]['rowSet'][i][5], "%Y-%m-%d") > date 
        and
        team_data['resultSets'][0]['rowSet'][i][7] == 'W'):
            
            wins_after_date +=1
    
        elif (team_data['resultSets'][0]['rowSet'][i][1] ==int(team_id) and 
        datetime.datetime.strptime(team_data['resultSets'][0]['rowSet'][i][5], "%Y-%m-%d") > date 
        and
        team_data['resultSets'][0]['rowSet'][i][7] == 'L'):
            
            loss_after_date +=1
    
    return {'wins_before_date': wins_before_date,
            'loss_before_date':loss_before_date,
            'wins_after_date': wins_after_date, 
            'loss_after_date':loss_after_date}            

player_trans_affect_raw = {}
for item in transaction_info:
    win_loss_dict = team_success(item[1],item[2])
    
    player_trans_affect_raw.setdefault(item[0], []) # item[0] = Player id
    player_trans_affect_raw[item[0]].append([item[1], win_loss_dict, item[4]]) # item[1] = team ID, item[4] = type of transaction

def trans_avg_score(win_loss_dict, trade_type):
    den = (win_loss_dict['wins_after_date'] + win_loss_dict['loss_after_date'])
    score = 0 # Default trade score?
    
    if den != 0:
        if trade_type in {'Signing', 'Trade', 'AwardonWaivers'}:
            score = float(win_loss_dict['wins_after_date'])/ den
        elif trade_type in {'Waive'}:
            score = float(win_loss_dict['wins_before_date'])/den
    
    return score
    
player_trans_affect = {}
for key in player_trans_affect_raw.keys():
    sum = 0
    for item in player_trans_affect_raw[key]:
        sum += trans_avg_score(item[1], item[2])
    avg = sum/len(player_trans_affect_raw[key])    
    
    player_trans_affect[key] = avg               
