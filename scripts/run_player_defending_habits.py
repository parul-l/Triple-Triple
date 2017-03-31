from triple_triple.class_player import create_player_class_instance
from triple_triple.startup_data import (
    get_df_raw_position_region,
    get_game_player_dict,
    get_game_info_dict,
    get_df_play_by_play
)
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play
import triple_triple.player_defending_habits as pdh
import triple_triple.player_possession_habits as pph
from triple_triple.players_in_game import get_players_in_game


game_player_dict = get_game_player_dict()
game_info_dict = get_game_info_dict()

df_raw_position_region = get_df_raw_position_region()
df_possession_region = pph.get_possession_df(
    dataframe=df_raw_position_region,
    has_ball_dist=2.0,
    len_poss=15
)

df_play_by_play = get_df_play_by_play()
df_game_stats = parse_df_play_by_play(df_play_by_play)

if __name__ == '__main__':
    game_id_list = [21500568]
    hometeam_id = game_info_dict['hometeam_id']
    awayteam_id = game_info_dict['visitorteam_id']

    home_player_id_list = get_players_in_game(
        df_raw_position=df_raw_position_region,
        team_id=hometeam_id
    )
    away_player_id_list = get_players_in_game(
        df_raw_position=df_raw_position_region,
        team_id=awayteam_id
    )

    home_player_class_dict = create_player_class_instance(
        player_list=home_player_id_list,
        game_player_dict=game_player_dict,
    )
    away_player_class_dict = create_player_class_instance(
        player_list=away_player_id_list,
        game_player_dict=game_player_dict,
    )
    for player_class in home_player_class_dict.values():
        df_possession = pph.characterize_player_possessions(
            game_id=game_id_list[0],
            player_class=player_class,
            df_possession=df_possession_region,
            df_game_stats=df_game_stats
        )

    df_possession_defender = pdh.get_df_possession_defender(
        offense_players_dict=home_player_class_dict,
        df_possession_region=df_possession_region,
        df_raw_position_region=df_raw_position_region,
        defender_team_id=awayteam_id
    )

    for player_class in away_player_class_dict.values():
        # update possession outcome when defending
        pdh.update_nba_stats(
            player_class=player_class,
            season='2015-16',
            season_type='Regular Season'
        )

        pdh.poss_result_on_defense(
            defender_class=player_class,
            df_possession_defender=df_possession_defender,
            game_id=None
        )

        pdh.poss_result_on_defense_reg(
            defender_class=player_class,
            df_possession_defender=df_possession_defender,
            game_id=None
        )

        pdh.get_def_off_region_matrix(
            defender_class=player_class,
            df_possession_defender=df_possession_defender,
            game_id=None,
        )
