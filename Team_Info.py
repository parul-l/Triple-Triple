import requests
import json
import time


team_id = 1610612737 # Atlanta Hawks
HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
           'referer': 'http://stats.nba.com/scores/'
          }

def get_data(url):
    response = requests.get(url, headers = HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)

team_info = []

for i in range(30):
    base_url = "http://stats.nba.com/stats/teamdetails?teamID="   
    team_url = base_url + str(team_id)
    data = get_data(team_url)

    team_headers = [
        data['resultSets'][0]['headers'][0],    # Team_ID
        data['resultSets'][0]['headers'][1],    # Abbreviated City
        data['resultSets'][0]['headers'][2],    # Team Name
        data['resultSets'][0]['headers'][5],    # Arena
        data['resultSets'][0]['headers'][6],    # Arena Capacity
        ]

    team_info.append({
        team_headers[0] : data['resultSets'][0]['rowSet'][0][0],
        team_headers[1] : data['resultSets'][0]['rowSet'][0][1],
        team_headers[2] : data['resultSets'][0]['rowSet'][0][2],
        team_headers[3] : data['resultSets'][0]['rowSet'][0][5],                team_headers[4] : data['resultSets'][0]['rowSet'][0][6],
        })

    team_id +=1
     

      
    
