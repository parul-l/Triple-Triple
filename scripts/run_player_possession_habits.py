import triple_triple.player_possession_habits as pph

from triple_triple.team_shooting_side import get_initial_shooting_sides
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play

from triple_triple.startup_data import (
    get_df_play_by_play,
    get_df_raw_position_data,
    get_game_info_dict
)

df_raw_position_data = get_df_raw_position_data()
df_play_by_play = get_df_play_by_play()
game_info_dict = get_game_info_dict()
df_game_stats = parse_df_play_by_play(df_play_by_play)

initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_raw_position_data, game_info_dict)


if __name__ == '__main__':

    df_possession = pph.get_possession_df(
        df_raw_position_data=df_raw_position_data,
        has_ball_dist=2.0,
        len_poss=15
    )

    df_possession = pph.add_regions_to_df(df_possession, initial_shooting_side)
    df_possession_action = pph.add_empty_action_to_df_raw(df_possession)

    game_id_list = [21500568]
#    player_id_list = [2547, 2548, 203110, 201939]
    player_id_list = [2547]
    
    df_possession_action = pph.get_multi_games_players_possessions(
        game_id_list=game_id_list,
        player_id_list=player_id_list,
        df_possession_action=df_possession_action,
        df_game_stats=df_game_stats
    )
