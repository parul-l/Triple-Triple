import json
import os

from triple_triple.config import DATASETS_DIR
import triple_triple.data_generators.get_data as gd
from triple_triple.data_generators.team_ids import get_team_ids


if __name__ == '__main__':

    base_url = 'http://stats.nba.com/stats/leaguedashteamstats'

    # all these parameters appear to be necessary
    params = {
        'Conference': '',
        'DateFrom': '',
        'DateTo': '',
        'Division': '',
        'GameScope': '',
        'GameSegment': '',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'MeasureType': 'Base',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': '2015-16',
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference': '',
        'VsDivision': '',
    }

    team_data = gd.get_data(base_url, params)
    team_ids, team_ids_rev = get_team_ids(team_data)

    # Save the files as jsons (they become strings when opened)
    json_file = open(os.path.join(DATASETS_DIR, 'team_ids.json'), 'wb')
    json.dump(team_ids, json_file)
