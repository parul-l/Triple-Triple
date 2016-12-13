import triple_triple.data_generators.player_game_stats_data as pgs_data
from triple_triple.nbastats_game_data import hometeam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_play_by_play,
)

game_id_dict = get_game_id_dict()
df_play_by_play = get_df_play_by_play()


if __name__ == '__main__':
    player_name = 'Chris Bosh'

    player_team_loc = pgs_data.player_team_loc_from_name(
        player_name,
        game_id_dict,
        hometeam_id
    )
    df_player_impact = pgs_data.player_impact_df(
        player_name,
        player_team_loc,
        game_id_dict,
        df_play_by_play
    )

    # returns list of list:
    # [[assist], [blocks], [commit_foul], [free_throw], [rebound], [shoot], [steal], [turnover]]
    player_game_stats = pgs_data.player_game_stats_nba(
        player_name,
        game_id_dict,
        df_player_impact
    )
