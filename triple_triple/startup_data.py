import cPickle as pickle
import json
import os

import pandas as pd

from triple_triple.config import DATASETS_DIR


def get_player_instances():
    filepath = os.path.join(DATASETS_DIR, 'player_instances.p')
    with open(filepath, 'rb') as json_file:
        return pickle.load(json_file)


def get_player_ids():
    filepath = os.path.join(DATASETS_DIR, 'player_ids.json')
    return json.load(open(filepath))


def get_game_info_dict():
    filepath = os.path.join(DATASETS_DIR, 'game_info_dict.json')
    with open(filepath, 'rb') as json_file:
        return pickle.load(json_file)


def get_game_player_dict():
    filepath = os.path.join(DATASETS_DIR, 'game_player_dict.json')
    with open(filepath, 'rb') as json_file:
        return pickle.load(json_file)


def get_df_raw_position_data():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_rawposition.csv')
    return pd.read_csv(filepath, low_memory=False)


def get_df_raw_position_region():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_rawposition_region.csv')
    return pd.read_csv(filepath, low_memory=False)


def get_df_play_by_play():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_nbaplaybyplay.csv')
    return pd.read_csv(filepath)


def get_df_box_score_player_tracking():
    # parse_date = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_box_score_player_tracking.csv')
    return pd.read_csv(filepath)
    # return pd.read_csv(filepath, parse_dates=['MIN'], date_parser=parse_date)


def get_df_box_score_traditional():
    # parse_date = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_box_score_traditional.csv')
    return pd.read_csv(filepath)
    # return pd.read_csv(filepath, parse_dates=['MIN'], date_parser=parse_date)


def get_df_player_bio_info():
    filepath = os.path.join(DATASETS_DIR, 'player_bio_info.csv')
    return pd.read_csv(filepath)


def get_df_all_game_info():
    filepath = os.path.join(DATASETS_DIR, 'df_all_game_info.csv')
    dtype_dict = {
        'game_id': str,
        'hometeam_id': str,
        'awayteam_id': str
    }
    return pd.read_csv(filepath, dtype=dtype_dict)


def get_player_possession_dataframes(json_file_name):
    with open(os.path.join(DATASETS_DIR, json_file_name), 'rb') as json_file:
        return pickle.load(json_file)
