import triple_triple.data_generators.player_position_data as ppd
from triple_triple.data_generators.player_game_stats_data import player_impact_df
from triple_triple.plot_player_game_stats import plot_player_game_info
from triple_triple.data_generators.nbastats_game_data import (
    teams_playing,
    play_by_play_df
)

from triple_triple.startup_data import (
    get_player_ids,
    get_df_all_game_info
)


df_game_info = get_df_all_game_info()

player_ids = get_player_ids()


base_url_play = 'http://stats.nba.com/stats/playbyplayv2'

if __name__ == '__main__':
    # January 11, 2016: MIA @ GSW
    game_id = '0021500568'
    player = 'Chris Bosh'
    params_play = {
        'EndPeriod': '10',      # default by NBA stats (acceptable values: 1, 2, 3, 4)
        'EndRange': '55800',    # not sure what this is
        'GameID': game_id,
        'RangeType': '2',       # not sure what this is
        'Season': '2015-16',
        'SeasonType': 'Regular Season',
        'StartPeriod': '1',     # acceptable values: 1, 2, 3, 4
        'StartRange': '0',      # not sure what this is
    }
    tracking_file = '/Users/pl/Downloads/' + game_id + '.json'

    data = ppd.open_json(tracking_file)
    game_id_dict = ppd.get_game_id_dict(data)

    hometeam_id, awayteam_id = teams_playing(game_id, df_game_info)

    df_positions = ppd.get_player_positions_df(data, game_id_dict)

    df_pos_dist = ppd.get_closest_to_ball_df(df_positions)

    df_play_by_play = play_by_play_df(base_url_play, params_play)

    df_player_impact = player_impact_df(player, hometeam_id, df_play_by_play)

    plot_player_game_info(player, df_player_impact, df_pos_dist)
