import triple_triple.class_game as class_game
import triple_triple.player_possession_habits as pph
import triple_triple.simulator.simulate_plays as sp

import triple_triple.simulator.create_teams as ct

from triple_triple.class_player import (
    create_player_class_instance,
    player_class_reset
)

from triple_triple.data_generators.player_bio_nbastats_data import (
    get_player_bio_df
)
from triple_triple.startup_data import (
    get_df_raw_position_region,
    get_game_player_dict,
    get_df_play_by_play,
    get_df_box_score_player_tracking,
    get_df_box_score_traditional
)
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play

from triple_triple.simulator_analytics.sim_result_stats import get_result_stats

df_raw_position_region = get_df_raw_position_region()
df_possession_region = pph.get_possession_df(
    dataframe=df_raw_position_region,
    has_ball_dist=2.0,
    len_poss=15
)

game_player_dict = get_game_player_dict()
df_play_by_play = get_df_play_by_play()
df_game_stats = parse_df_play_by_play(df_play_by_play)

reg_to_num = {
    'paint': 0,
    'mid_range': 1,
    'key': 2,
    'perimeter': 3,
    'back_court': 4,
    'out_of_bounds': 5
}


if __name__ == '__main__':
    team0_id_list = [203110, 202691, 201939, 101106, 201575]
    team1_id_list = [2547, 2548, 2736, 2617, 2405]
    
    team0_id_list = [201939, 201939]
    team1_id_list = [201939, 201939]
    game_id_list = [21500568]

    team0_class_dict, team1_class_dict = ct.get_complete_teams(
        team0_id_list,
        team1_id_list,
        game_id_list
    )

    df_player_bio = get_player_bio_df(
        player_id_list=(team0_id_list + team1_id_list)
    )

    hometeam_id = 1610612744
    awayteam_id = 1610612748

    # game class
    game_class = class_game.Game(
        hometeam_id=hometeam_id,
        awayteam_id=awayteam_id
    )

    ball_class_dict = create_player_class_instance(
        player_list=[-1],
        game_player_dict=game_player_dict,
        df_player_bio=None
    )

    ball_class = ball_class_dict[-1]

    # simulate 100 games
    # to re-do the simulation we reset the parameters
    # Assuming each play is about 20 seconds and each
    # play consists of 5 passes before an shot/turnover

    df_results_team0, df_results_team1, df_all_games = sp.simulate_multiple_games(
        num_sim_games=10,
        num_sim_actions=864,
        teams_list=[team0_class_dict, team1_class_dict],
        ball_class=ball_class,
        hometeam_id=hometeam_id,
        awayteam_id=awayteam_id
    )

    df_box_score_player_tracking = get_df_box_score_player_tracking()
    df_box_score_traditional = get_df_box_score_traditional()

    team0_actual, team1_actual, team0_sim_avg, team1_sim_avg, team0_sim_std, team1_sim_std = \
        get_result_stats(
            df_results_team0,
            df_results_team1,
            df_box_score_player_tracking,
            df_box_score_traditional,
            teams_list=[team0_class_dict, team1_class_dict],
            hometeam_id=hometeam_id,
            awayteam_id=awayteam_id
        )

    # simulate 1 game
    df_data = sp.sim_plays(
        num_sim=864,
        teams_list=[team0_class_dict, team1_class_dict],
        game_class=game_class,
        ball_class=ball_class
    )

    player_class_reset(team0_class_dict)
    player_class_reset(team1_class_dict)
    class_game.game_class_reset(game_class)

    # print player's outcome
    for player_class in team0_class_dict.values():
        print player_class.name
        print 'region', player_class.court_region
        print 'possession', player_class.has_possession
        print 'defender', player_class.defended_by
        print 'passes', player_class.passes
        print 'two_pt_shot_attempts', player_class.two_pt_shot_attempts
        print 'two_pt_shots_made', player_class.two_pt_shots_made
        print 'three_pt_shot_attempts', player_class.three_pt_shot_attempts
        print 'three_pt_shots_made', player_class.three_pt_shots_made
        print 'turnovers', player_class.turnovers
        print 'total_points', player_class.total_points
        print ""

    # print player's outcome
    for player_class in team1_class_dict.values():
        print player_class.name
        print 'region', player_class.court_region
        print 'possession', player_class.has_possession
        print 'defender', player_class.defended_by
        print 'passes', player_class.passes
        print 'two_pt_shot_attempts', player_class.two_pt_shot_attempts
        print 'two_pt_shots_made', player_class.two_pt_shots_made
        print 'three_pt_shot_attempts', player_class.three_pt_shot_attempts
        print 'three_pt_shots_made', player_class.three_pt_shots_made
        print 'turnovers', player_class.turnovers
        print 'total_points', player_class.total_points
        print ""

    # print game outcome
    print 'score', game_class.score
    print 'num_plays', game_class.num_plays
    print 'two_pt_shots_attempts', game_class.two_pt_shot_attempts
    print 'two_pt_shots_made', game_class.two_pt_shots_made
    print 'three_pt_shot_attempts', game_class.three_pt_shot_attempts
    print 'three_pt_shots_made', game_class.three_pt_shots_made
    print 'off_rebounds', game_class.off_rebounds
    print 'def_rebounds', game_class.def_rebounds
    print 'steals', game_class.steals
    print 'blocks', game_class.blocks
    print 'turnovers', game_class.turnovers
    print 'passes', game_class.passes
