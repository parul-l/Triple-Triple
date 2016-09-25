import requests
import json
import pandas as pd

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)' 
                          'AppleWebKit/537.36 (KHTML, like Gecko)' 
                          'Chrome/51.0.2704.103 Safari/537.36'),
           'referer':     'http://stats.nba.com/player/'
          }
 
# Game data statistics for every game in the specified season(s)
base_url_game = "http://stats.nba.com/stats/leaguegamelog"
params_game = {'Counter':'1000',
               'DateFrom':'',
               'DateTo':'',
               'Direction':'DESC',
               'LeagueID':'00',
               'PlayerOrTeam':'T',
               'Season':'2015-16',
               'SeasonType':'Regular Season',
               'Sorter':'PTS'
               }
               

# January 11, 2016, MIA @ GSW                 
# play by play data
end_period = '10'           # default by NBA stats. Customize to 1,2,3,4
end_range  = '55800'        # not sure what this is
game_id = '0021500568'      # game_id
range_type = '2'            # not sure
season_year = '2015-16'            
season_type = 'Regular Season'   # 'Playoffs' or 'Regular Season'
start_period = '1'          # default by NBA stats. Customize to 1, 2, 3, 4
start_range = '0'           # not sure       

base_url_play = 'http://stats.nba.com/stats/playbyplayv2'
params_play = {'EndPeriod':end_period,
          'EndRange':end_range,
          'GameID':game_id,
          'RangeType':range_type,
          'Season':season_year,
          'SeasonType':season_type,
          'StartPeriod':start_period,
          'StartRange':start_range,
          }
###############################################################
###############################################################          
def get_data(base_url, params, headers):
    response = requests.get(base_url, params = params, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)   
###############################################################
###############################################################
# Game data statistics for every game in the specified season(s)
all_games_stats_in_season = get_data(base_url_game, params_game, HEADERS)

# find info with given game_ids (2 rows, 1 for each team)

def teams_playing(game_id, all_games_stats_for_season):
    game_info = [item for item in all_games_stats_for_season['resultSets'][0]['rowSet'] if  
                item[4]==game_id]
                
    if game_info[0][6].split()[1]=='vs.':
        home_team = game_info[0][1]
        away_team = game_info[1][1]
    elif game_info[0][6].split()[1]=='@':
        home_team = game_info[1][1]
        away_team = game_info[0][1]  
    
    return home_team, away_team     
    
###############################################################
###############################################################
# play by play data        
def time_in_seconds(time):
    t = time.split(':')
    return int(t[0])*60 + int(t[1])

def score_in_int(score):
    try: 
        new_score = [int(score.split('-')[0]),
        int(score.split('-')[1])]
        return new_score     
    
    except:
        new_score = score
        return new_score   
            
def play_by_play_df(base_url_play, params_play, HEADERS):            
    play_data = get_data(base_url_play, params_play, HEADERS)        
          
    headers_play_by_play = ["Game_ID",
                            "PERIOD",
                            "WCTIMESTRING",
                            "PCTIMESTRING",
                            "HOMEDESCRIPTION",
                            "NEUTRAL DESCRIPTION",
                            "VISITORDESCRIPTION",
                            "SCORE",  #[Away, Home]
                            "PLAYER1_ID",
                            "PLAYER1_NAME",
                            "PLAYER1_TEAM_ID",
                            "PLAYER2_ID",
                            "PLAYER2_NAME",
                            "PLAYER2_TEAM_ID",
                            "PLAYER3_ID",
                            "PLAYER3_NAME",
                            "PLAYER3_TEAM_ID"]      

    play_by_play = []        
    len_plays = len(play_data['resultSets'][0]['rowSet'])

    for i in range(len_plays):
        play_by_play.append(
        [
        play_data['resultSets'][0]['rowSet'][i][0],
        play_data['resultSets'][0]['rowSet'][i][4],
        play_data['resultSets'][0]['rowSet'][i][5],
        time_in_seconds(play_data['resultSets'][0]['rowSet'][i][6]),
        play_data['resultSets'][0]['rowSet'][i][7],
        play_data['resultSets'][0]['rowSet'][i][8],
        play_data['resultSets'][0]['rowSet'][i][9],
        score_in_int(play_data['resultSets'][0]['rowSet'][i][10]),
        play_data['resultSets'][0]['rowSet'][i][13],
        play_data['resultSets'][0]['rowSet'][i][14],
        play_data['resultSets'][0]['rowSet'][i][15],
        play_data['resultSets'][0]['rowSet'][i][20],
        play_data['resultSets'][0]['rowSet'][i][21],
        play_data['resultSets'][0]['rowSet'][i][22],
        play_data['resultSets'][0]['rowSet'][i][27],
        play_data['resultSets'][0]['rowSet'][i][28],
        play_data['resultSets'][0]['rowSet'][i][29]
        ])
        
    # create a data frame from the list
    return pd.DataFrame(play_by_play, columns = headers_play_by_play) 

if __name__=='__main__':
    df_play_by_play = play_by_play_df(base_url_play, params_play, HEADERS)

    # Save file for future ease
    df_play_by_play.to_csv('MIA_GSW_nbaplaybyplay.csv')   
