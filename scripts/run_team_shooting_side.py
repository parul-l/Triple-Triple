from triple_triple.import_postgres_tables import get_game_specific_tables
from triple_triple.team_shooting_side import get_initial_shooting_sides


if __name__ == '__main__':
    game_id = '0021500492'
    df_dict = get_game_specific_tables(game_id)
    shooting_side = get_initial_shooting_sides(
        df_games=df_dict['df_games'],
        df_play_by_play=df_dict['df_play_by_play'],
        df_game_positions=df_dict['df_game_positions']
    )
