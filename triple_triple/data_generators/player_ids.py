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


def get_data(base_url, params, headers=HEADERS):
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        print(response.status_code)

# To compare basketball-reference and nba.com,
# we format the names in the 'same' way but
# some discrepancies still exist
def remove_unwanted_char(some_string):
    return some_string.replace('.', '').replace('*', '')

def all_player_ids(player_info_list):
    player_ids = {}
    len_players = len(player_info_list)
    
    for i in range(len_players):
        player_ids[player_info_list[i][0]] = (
            player_info_list[i][1],   # last, first
            remove_unwanted_char(player_info_list[i][2]), # first last name
            int(player_info_list[i][4]), # From
            int(player_info_list[i][5]) # To
        )
        
    return player_ids


if __name__=='__main__':
    # allowable entries for IsOnlyCurrentSeason is '0' or '1'.
    # 0 implies show all players up to and including chosen season
    # 1 imples show only players up to current season
    base_url = 'http://stats.nba.com/stats/commonallplayers'
    params = {
        'IsOnlyCurrentSeason': '0',
        'LeagueID': '00',
        'Season': '2016-17'
    }
    
    data = get_data(base_url, params, HEADERS)
    player_ids = all_player_ids(data['resultSets'][0]['rowSet'])

    # reverse order to compare with player_bios
    player_ids_rev = dict((v, k) for k, v in player_ids.iteritems())      

    # Save the files as jsons but they become strings?
    json_file = open(os.path.join(DATASETS_DIR, 'player_ids.json'), 'wb')
    json.dump(player_ids, json_file)

    # Save the files as jsons: This one doesn't work because key is a tuple?
    # json.dump(player_ids_rev, open('player_ids_rev.json', 'wb'))   
         
