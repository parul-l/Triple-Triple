import os
from triple_triple.config import DATASETS_DIR
import triple_triple.player_possession_habits as pph

from triple_triple.team_shooting_side import get_initial_shooting_sides
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play
from triple_triple.class_player import create_player_class_instance

from triple_triple.startup_data import (
    get_df_play_by_play,
    get_df_raw_position_data,
    get_df_raw_position_region,
    get_game_info_dict,
    get_game_player_dict
)

df_raw_position_data = get_df_raw_position_data()
df_raw_position_region = get_df_raw_position_region()
game_info_dict = get_game_info_dict()
game_player_dict = get_game_player_dict()
df_play_by_play = get_df_play_by_play()
df_game_stats = parse_df_play_by_play(df_play_by_play)

initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_raw_position_data, game_info_dict)


if __name__ == '__main__':

    df_possession = pph.get_possession_df(
        dataframe=df_raw_position_data,
        has_ball_dist=2.0,
        len_poss=15
    )

    df_possession = pph.add_regions_to_df(df_possession, initial_shooting_side)

    # df_raw_position_region = pph.add_regions_to_df(df_raw_position_data, initial_shooting_side)
    # 
    # filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_rawposition_region.csv')
    # df_raw_position_region.to_csv(filepath, index=False)


    game_id_list = [21500568]
    player_id_list = [2547, 2548]

    player_class_dict = create_player_class_instance(
        player_list=player_id_list,
        game_player_dict=game_player_dict,
    )

    for player_class in player_class_dict.values():
        df_possession = pph.characterize_player_possessions(
            game_id=game_id_list[0],
            player_class=player_class,
            df_possession=df_possession,
            df_game_stats=df_game_stats
        )

    defender_team_id = pph.get_defender_team_id(
        players_dict=player_class_dict,
        initial_shooting_side=initial_shooting_side
    )

    df_possession_defender = pph.get_df_possession_defender(
        players_dict=player_class_dict,
        df_possession_region=df_possession,
        df_raw_position_region=df_raw_position_region,
        defender_team_id=defender_team_id
    )
