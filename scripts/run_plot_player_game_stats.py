import triple_triple.data_generators.player_position_data as ppd

from triple_triple.data_generators.player_game_stats_data import (
    player_impact_df,
    player_team_loc_from_name
)
from triple_triple.plot_player_game_stats import plot_player_game_info
from triple_triple.data_generators.nbastats_game_data import teams_playing
from triple_triple.startup_data import (
    get_df_positions,
    get_df_play_by_play,
    get_df_all_game_info,
    get_game_id_dict)


df_game_info = get_df_all_game_info()

base_url_play = 'http://stats.nba.com/stats/playbyplayv2'

if __name__ == '__main__':
    # January 11, 2016: MIA @ GSW
    game_id = '0021500568'
    player = 'Chris Bosh'

    game_id_dict = get_game_id_dict()

    hometeam_id, awayteam_id = teams_playing(game_id, df_game_info)

    df_positions = get_df_positions()

    df_pos_dist = ppd.get_closest_to_ball_df(df_positions)

    df_play_by_play = get_df_play_by_play()

    player_team_loc = player_team_loc_from_name(
        player,
        game_id_dict,
        hometeam_id
    )
    df_player_impact = player_impact_df(
        player,
        player_team_loc,
        game_id_dict,
        df_play_by_play
    )

    plot_player_game_info(player, game_id_dict, df_player_impact, df_pos_dist)
