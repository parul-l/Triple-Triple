# This player bio info is obtained from two sources
# 1. NBA stats (very slow - approx 35min)
# 2. basketball-reference.com

#######################################################
# From NBA STATS (total player list length: 4186)
# See Web Scraping file for comparison
#######################################################

import json
import requests
import numpy as np
import pandas as pd

from triple_triple.startup_data import get_player_ids


player_ids = get_player_ids()

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/51.0.2704.103 Safari/537.36'),
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

def get_player_bio_df(base_url, params, player_ids):
    player_bio_info = []
    bad_keys = []

    for key in player_ids.keys():
        try:
            playerid = str(key)
            # add playerid to params
            params['PlayerID'] = playerid
            player_data = get_data(base_url, params)

            player_bio_info.append([
                player_data['resultSets'][0]['rowSet'][0][0],  # id
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

    bio_headers = [
        'Player_ID',
        'Player_Name',
        'From',
        'To',
        'Position',
        'Height',
        'Weight',
        'Birthdate'
    ]

    return pd.DataFrame(player_bio_info, columns=bio_headers)

##########################
##########################

if __name__ == '__main__':

    # from NBA stats:
    base_url = 'http://stats.nba.com/stats/commonplayerinfo'
    params = {
        'GraphEndSeason': '2016-17',
        'GraphStartSeason': '2016-17',
        'GraphStat': 'PTS',
        'LeagueID': '00',
        'MeasureType': 'Base',
        'PerMode': 'PerGame',
        'SeasonType': 'Regular Season',
        'SeasonType': 'Playoffs'
    }

    df_player_bio_nbastats = get_player_bio_df(base_url, params)

    # Save file
    # df_player_bio.to_csv('triple_triple/data/player_bio_info_nbastats.csv')
