import pandas as pd
from triple_triple.data_generators.get_data import get_data

base_url = 'http://stats.nba.com/stats/leaguedashplayerstats'
params = {
    'College': '',
    'Conference': '',
    'Country': '',
    'DateFrom': '',
    'DateTo': '',
    'Division': '',
    'DraftPick': '',
    'DraftYear': '',
    'GameScope': '',
    'GameSegment': '',
    'Height': '',
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
    'Weight': ''
}


def get_player_stats_df(
    base_url=base_url,
    params=params,
    season='2015-16',
    season_type='Regular Season'
):
    # update params if need be
    params['Season'] = season
    params['SeasonType'] = season_type

    data = get_data(base_url=base_url, params=params)
    info_list = data['resultSets'][0]['rowSet']
    player_stats = []

    for player_info in info_list:
        player_stats.append([
            player_info[0],     # player_id
            player_info[1],     # player_name
            player_info[2],     # team_id
            player_info[5],     # games played
            player_info[24],    # steals
            player_info[25],    # blocks
            player_info[19],    # off_rebounds
            player_info[20],    # def_rebounds
            player_info[18],    # free_throw_pct
            player_info[27],    # personal_fouls

        ])

    headers = [
        'player_id',
        'player_name',
        'team_id',
        'games_played',
        'steals',
        'blks',
        'off_rebounds',
        'def_rebounds',
        'free_throw_pct',
        'personal_fouls',
    ]

    return pd.DataFrame(data=player_stats, columns=headers)
