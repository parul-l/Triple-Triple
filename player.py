import json
import requests
from player_bio import player_bio_info
from player_bio import df_player_bio

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
           'referer':     'http://stats.nba.com/player/'
          }

# allowable entries for only_current is '0' or '1'.
# 0 implies show all players up to and including chosen season
# 1 imples show only players up to current season
only_current = '1'
league_id = '00'
current_season = '1998-99'
    

base_url = 'http://stats.nba.com/stats/commonallplayers'
params = {'IsOnlyCurrentSeason': only_current,
          'LeagueID': league_id,
          'Season':   current_season
          }


def get_data(base_url):
    response = requests.get(base_url, params = params, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)
        
data = get_data(base_url)

player_headers = [
    data['resultSets'][0]['headers'][0],    # Person_ID
    data['resultSets'][0]['headers'][1],    # Last, First
    data['resultSets'][0]['headers'][3],    # Roster Status
    data['resultSets'][0]['headers'][4],    # From Year
    data['resultSets'][0]['headers'][5],    # To Year
    data['resultSets'][0]['headers'][7],    # Team ID
    data['resultSets'][0]['headers'][9]     # Team_Name
]        

table = soup.find('table', {'class': 'sortable  stats_table', 'id':'players'})

for row in table.findAll("tr"):
    cells = row.findAll("td")
    print cells.text

tables = soup.findChildren('table')
my_table = tables[0]
rows = my_table.findChildren(['tr'])

player_bio_info = []
for row in rows:
    cells = row.findChildren('td')
    try:
        temp_list= [cells[0].text, 
                    cells[1].text, 
                    cells[2].text, 
                    cells[3].text, 
                    cells[4].text,   
                    cells[5].text, 
                    cells[6].text]
        player_bio_info.append(temp_list)
    except:
        print row                      
