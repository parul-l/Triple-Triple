import os
import numpy as np
import pandas as pd

from triple_triple.config import MOCK_DATASETS_DIR


def rand_coord_generator(lower_bound, upper_bound, len_array):
    t = np.random.random(len_array)
    return (1 - t) * lower_bound + t * upper_bound


def make_mock_df():
    headers = [
        'game_clock',
        'shot_clock',
        'period',
        'team_id',
        'player_ids',
        'player_jersey',
        'x_loc',
        'y_loc'
    ]
    game_clock = np.array(np.arange(14, 8, -1)).repeat(5)
    shot_clock = np.array(np.arange(10, 4, -1)).repeat(5)
    period = np.array([1, 2, 3]).repeat(10)
    team_ids = np.tile([-1, 100, 100, 222, 222], 6)
    player_ids = np.tile(np.arange(-1, 4), 6)
    player_jersey = np.tile([-1, 51, 52, 53, 54], 6)
    x_loc = rand_coord_generator(lower_bound=47, upper_bound=94, len_array=30)
    y_loc = rand_coord_generator(lower_bound=0, upper_bound=50, len_array=30)

    mock_df = pd.DataFrame(
        data=np.array([
            game_clock,
            shot_clock,
            period,
            team_ids,
            player_ids,
            player_jersey,
            x_loc,
            y_loc
        ]).T,
        columns=headers)

    return mock_df


def save_df_raw_position_data_region_snippet(
    df_raw_position_region,
    idx_start_slice=2000,
    idx_end_slice=2005
):
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_raw_position_region_snippet.csv')

    df_raw_position_region[idx_start_slice:idx_end_slice]\
        .to_csv(filepath)


def open_df_raw_position_data_region_snippet():
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_raw_position_region_snippet.csv')
    parse_dates = ['game_date']
    return pd.read_csv(filepath, parse_dates=parse_dates)


def save_df_possession_region_snippet(
    df_possession_region,
    idx_start_slice=2014,
    idx_end_slice=2024
):
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_possession_region_snippet.csv')

    df_possession_region[idx_start_slice:idx_end_slice]\
        .to_csv(filepath)


def open_df_possession_region_snippet():
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_possession_region_snippet.csv')
    parse_dates = ['game_date']
    return pd.read_csv(filepath, parse_dates=parse_dates)


def save_df_play_by_play_snippet(
    df_play_by_play,
    idx_start_slice=0,
    idx_end_slice=10
):
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_play_by_play_snippet.csv')

    df_play_by_play[idx_start_slice:idx_end_slice]\
        .to_csv(filepath)


def open_df_play_by_play_snippet():
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_play_by_play_snippet.csv')
    return pd.read_csv(filepath)


def save_df_game_stats_snippet(
    df_game_stats,
    idx_start_slice=0,
    idx_end_slice=10
):
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_game_stats_snippet.csv')

    df_game_stats[idx_start_slice:idx_end_slice]\
        .to_csv(filepath)


def open_df_game_stats_snippet():
    filepath = os.path.join(MOCK_DATASETS_DIR, 'df_game_stats_snippet.csv')
    return pd.read_csv(filepath)
