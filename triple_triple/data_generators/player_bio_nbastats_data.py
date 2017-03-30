#######################################################
# From NBA STATS (total player list length: 4186)
# See Web Scraping file for comparison
#######################################################
import pandas as pd

import triple_triple.data_generators.get_data as gd
from triple_triple.startup_data import get_player_ids


player_ids = get_player_ids()


def get_player_bio_df(base_url, params, player_ids):
    player_bio_info = []
    bad_keys = []

    for key in player_ids.keys():
        try:
            playerid = str(key)
            # add playerid to params
            params['PlayerID'] = playerid
            player_data = gd.get_data(base_url, params)

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
        'player_id',
        'player_name',
        'from',
        'to',
        'position',
        'height',
        'weight',
        'birthdate'
    ]

    return pd.DataFrame(player_bio_info, columns=bio_headers)


# Get active player info only
def get_active_player_bio_df(url):
    data = gd.get_data(url, {})
    player_bio_info = []

    for player_dict in data:
        player_bio_info.append([
            int(player_dict['personId']),
            player_dict['displayName'],
            player_dict['pos'],
            int(player_dict['heightFeet']) * 12 + int(player_dict['heightInches']),
            int(player_dict['weightPounds'])
        ])

    bio_headers = [
        'player_id',
        'player_name',
        'position',
        'height',
        'weight',
    ]

    return pd.DataFrame(player_bio_info, columns=bio_headers)
