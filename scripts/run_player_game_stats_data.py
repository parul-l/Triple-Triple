from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play
from triple_triple.startup_data import get_df_play_by_play

df_play_by_play = get_df_play_by_play()


if __name__ == '__main__':

    df_game_stats = parse_df_play_by_play(df_play_by_play)
