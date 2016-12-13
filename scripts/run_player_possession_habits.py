import triple_triple.player_possession_habits as pph
from triple_triple.team_shooting_side import initial_shooting_side

from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_pos_dist,
    get_df_pos_dist_trunc,
    get_df_play_by_play,
)


if __name__ == '__main__':

    player_name = 'Chris Bosh'

    reg_to_num = {
        'back court': 0,
        'mid-range': 1,
        'key': 2,
        'out of bounds': 3,
        'paint': 4,
        'perimeter': 5
    }

    game_id_dict = get_game_id_dict()

    df_pos_dist = get_df_pos_dist()
    df_pos_dist_trunc = get_df_pos_dist_trunc()
    df_play_by_play = get_df_play_by_play()

    df_pos_dist_reg = pph.get_player_court_region_df(
        df_pos_dist,
        initial_shooting_side,
        hometeam_id,
        awayteam_id
    )
    df_pos_dist_reg_trunc = pph.get_pos_trunc_df(df_pos_dist_reg)
    player_poss_idx = pph.player_possession_idx(player_name, df_pos_dist_trunc)

    # returns list of lists
    # [play_shot, play_assist, play_turnover, start_idx_used, end_idx_used]

    known_player_possessions = pph.characterize_player_possessions(
        player_name,
        game_id_dict,
        df_pos_dist_trunc,
        player_poss_idx,
        hometeam_id,
        awayteam_id,
        initial_shooting_side,
        df_play_by_play
    )

    play_pass = pph.get_pass_not_assist(
        player_name,
        df_pos_dist_trunc,
        known_player_possessions,
        player_poss_idx,
        initial_shooting_side,
        hometeam_id,
        awayteam_id,
        t=10
    )

    df_player_possession = pph.result_player_possession_df(known_player_possessions, play_pass)

    possession_dict = {
        'play_pass': play_pass,
        'df_player_possession': df_player_possession,
        'known_player_possessions': known_player_possessions,
        'player_poss_idx': player_poss_idx,
        'df_pos_dist_reg': df_pos_dist_reg
    }

    # save file to use in run_simulate_player_positions
    pph.save_player_poss_dict('test_save.json', possession_dict)

    # plot_coord = plot_team_possession(df_pos_dist_trunc, 10,20, hometeam_id, awayteam_id)
