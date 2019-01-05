import os

from triple_triple.config import DATASETS_DIR
from triple_triple.data_generators.all_games_info import all_games_info_df
import triple_triple.data_generators.get_data as gd

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

# game data statistics for every game in the specified season(s)
all_games_stats_data = gd.get_data(base_url_game, params_game)

if __name__ == '__main__':

    df_all_game_info = all_games_info_df(all_games_stats_data)

    # save file for future ease
    filepath = os.path.join(DATASETS_DIR, 'df_all_game_info.csv')
    df_all_game_info.to_csv(filepath)
