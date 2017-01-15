import cPickle as pickle
import os
from triple_triple.config import DATASETS_DIR
from triple_triple.data_generators import player_position_data as ppd

# January 11, 2016: MIA @ GSW
game_id = '0021500568'

if __name__ == '__main__':

    tracking_file = '/Users/pl/Downloads/' + game_id + '.json'

    data = ppd.open_json(tracking_file)
    game_info_dict = ppd.get_game_info(data)
    game_player_dict = ppd.get_game_player_dict(data)
    df_raw_position_data = ppd.get_raw_position_data_df(
        data=data,
        game_player_dict=game_player_dict,
        game_info_dict=game_info_dict
    )


    # 
    # df_positions = ppd.get_player_positions_df(data, game_player_dict)
    # df_pos_dist = ppd.get_closest_to_ball_df(df_positions)
    # df_pos_dist_trunc = ppd.get_df_pos_trunc(df_pos_dist, has_ball_dist=2)

    # save files
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_rawposition.csv')
    df_raw_position_data.to_csv(filepath)

    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_positions.csv')
    df_positions.to_csv(filepath, index=False, tupleize_cols=False, float_format='%.8f')

    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_pos_dist.csv')
    df_pos_dist.to_csv(filepath, index=False, tupleize_cols=False, float_format='%.8f')

    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_pos_dist_trunc.csv')
    df_pos_dist_trunc.to_csv(filepath, index=False, tupleize_cols=False, float_format='%.8f')

    # save game_info_dict
    # save the files as jsons but they open as strings
    filepath = os.path.join(DATASETS_DIR, 'game_info_dict.json')
    with open(filepath, 'wb') as json_file:
        pickle.dump(game_info_dict, json_file)

    # save game_player_dict
    # save the files as jsons but they open as strings
    filepath = os.path.join(DATASETS_DIR, 'game_player_dict.json')
    with open(filepath, 'wb') as json_file:
        pickle.dump(game_player_dict, json_file)
