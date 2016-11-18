import triple_triple.data_generators.player_game_stats_data as pgs_data
from save_playbyplay import hometeam_id


if __name__ == '__main__':
    player = 'Chris Bosh'

    df_player_impact = pgs_data.player_impact_df(player, hometeam_id)
    player_game_stats = pgs_data.player_game_stats_nba(player, df_player_impact)
