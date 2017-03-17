import triple_triple.player_possession_habits as pph
import triple_triple.data_generators.nbastats_game_data as ngd

from triple_triple.startup_data import (
    get_df_raw_position_region,
    get_game_player_dict,
    get_game_info_dict
)

df_raw_position_region = get_df_raw_position_region()
game_player_dict = get_game_player_dict()
game_info_dict = get_game_info_dict()

if __name__ == '__main__':
    game_id_list = ['0021500568']
    
    base_url_box_score = 'http://stats.nba.com/stats/boxscoreplayertrackv2'
    params_box_score = {
        'EndPeriod': '10',
        'EndRange': '55800',
        'GameID': game_id_list[0],
        'RangeType': '2',
        'Season': '2015-16',
        'SeasonType': 'Regular Season',
        'StartPeriod': '1',
        'StartRange': '0'
    }

    df_box_score = ngd.box_score_df(
        base_url_box_score,
        params_box_score
    )

    hometeam_id = game_info_dict['hometeam_id']
    visitorteam_id = game_info_dict['visitorteam_id']

    # player_id_lists
    home_player_id_list = df_box_score.query('TEAM_ID==@hometeam_id').PLAYER_ID.values
    
    visitor_player_id_list = df_box_score.query('TEAM_ID==@visitorteam_id').PLAYER_ID.values
