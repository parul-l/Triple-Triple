import triple_triple.data_generators.player_bio_nbastats_data as pbd_nba

from triple_triple.startup_data import get_player_ids


player_ids = get_player_ids()

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

    df_player_bio_nbastats = pbd_nba.get_player_bio_df(base_url, params, player_ids)

    # Save file
    # df_player_bio.to_csv('triple_triple/data/player_bio_info_nbastats.csv')
