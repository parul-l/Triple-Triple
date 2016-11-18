import json
import os
import triple_triple.data_generators.player_ids as player_ids
import triple_triple.data_generators.get_data as gd

from triple_triple.config import DATASETS_DIR

if __name__ == '__main__':

    # allowable entries for IsOnlyCurrentSeason is '0' or '1'.
    # 0 implies show all players up to and including chosen season
    # 1 imples show only players up to current season
    base_url = 'http://stats.nba.com/stats/commonallplayers'
    params = {
        'IsOnlyCurrentSeason': '0',
        'LeagueID': '00',
        'Season': '2016-17'
    }

    data = gd.get_data(base_url, params)
    player_ids = player_ids.all_player_ids(data['resultSets'][0]['rowSet'])

    # reverse order to compare with player_bios
    player_ids_rev = dict((v, k) for k, v in player_ids.iteritems())

    # Save the files as jsons but they become strings?
    json_file = open(os.path.join(DATASETS_DIR, 'player_ids.json'), 'wb')
    json.dump(player_ids, json_file)

    # Save the files as jsons: This one doesn't work because key is a tuple?
    # json.dump(player_ids_rev, open('player_ids_rev.json', 'wb'))
