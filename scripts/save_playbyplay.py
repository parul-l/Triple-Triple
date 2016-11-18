import os

from triple_triple.config import DATASETS_DIR
import triple_triple.data_generators.get_data as gd
from triple_triple.data_generators import nbastats_game_data as ngd


# January 11, 2016, MIA @ GSW play by play data
game_id = '0021500568'

base_url_game = "http://stats.nba.com/stats/leaguegamelog"
params_game = {
    'Counter': '1000',
    'DateFrom': '',
    'DateTo': '',
    'Direction': 'DESC',
    'LeagueID': '00',
    'PlayerOrTeam': 'T',
    'Season': '2015-16',
    'SeasonType': 'Regular Season',
    'Sorter': 'PTS'
}

base_url_play = 'http://stats.nba.com/stats/playbyplayv2'
params_play = {
    'EndPeriod': '10',      # default by NBA stats (acceptablevalues: 1, 2, 3, 4)
    'EndRange': '55800',    # not sure what this is
    'GameID': game_id,
    'RangeType': '2',       # not sure what this is
    'Season': '2015-16',
    'SeasonType': 'Regular Season',
    'StartPeriod': '1',     # acceptable values: 1, 2, 3, 4
    'StartRange': '0',      # not sure what this is
}

base_url_box_score = 'http://stats.nba.com/stats/boxscoreplayertrackv2'
params_box_score = {
    'EndPeriod': '10',
    'EndRange': '55800',
    'GameID': game_id,
    'RangeType': '2',
    'Season': '2015-16',
    'SeasonType': 'Regular Season',
    'StartPeriod': '1',
    'StartRange': '0'
}

# game data statistics for every game in the specified season(s)
all_games_stats = gd.get_data(base_url_game, params_game)
hometeam_id, awayteam_id = ngd.teams_playing(game_id, all_games_stats)

if __name__ == '__main__':

    df_play_by_play = ngd.play_by_play_df(
        base_url_play,
        params_play
    )

    df_box_score = ngd.box_score_df(
        base_url_box_score,
        params_box_score
    )

    # save files for future ease
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_nbaplaybyplay.csv')
    df_play_by_play.to_csv(filepath)

    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_box_score.csv')
    df_box_score.to_csv(filepath)
