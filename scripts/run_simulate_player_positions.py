import copy
import triple_triple.player_defending_habits as pdh
import triple_triple.player_possession_habits as pph
import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp

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
    get_df_play_by_play
)
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play


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
    'back court': 0,
    'mid-range': 1,
    'key': 2,
    'out of bounds': 3,
    'paint': 4,
    'perimeter': 5
}


if __name__ == '__main__':
    team1_id_list = [203110, 202691, 201939, 101106, 201575]
    team2_id_list = [2547, 2548, 2736, 2617, 2405]
    game_id_list = [21500568]
        
    df_player_bio = get_player_bio_df(
        player_id_list=(team1_id_list + team2_id_list)
    )

    # this is weird since this will only have one element
    ball_class_dict = create_player_class_instance(
        player_list=[-1],
        game_player_dict=game_player_dict,
        df_player_bio=None
    )

    ball_class = ball_class_dict[-1]

    team1_class_dict = create_player_class_instance(
        player_list=team1_id_list,
        game_player_dict=game_player_dict,
        df_player_bio=df_player_bio
    )
    team2_class_dict = create_player_class_instance(
        player_list=team2_id_list,
        game_player_dict=game_player_dict,
        df_player_bio=df_player_bio
    )

    team1_id = team1_class_dict[team1_id_list[0]].team_id
    team2_id = team2_class_dict[team2_id_list[0]].team_id

    # combine dictionaries to update both dictionaries together
    combined_players_dict = copy.copy(team1_class_dict)
    combined_players_dict.update(team2_class_dict)

    for player_class in combined_players_dict.values():
        # update region probability
        ppp.update_region_prob_matrix(
            player_class=player_class,
            game_id=game_id_list[0],
            game_player_dict=game_player_dict,
            df_raw_position_region=df_raw_position_region,
            player_possession=False,
            team_on_offense=True,
            team_on_defense=False,
            half_court=True
        )

        # update df_possessions using NBA df_game_stats info
        df_possession = pph.characterize_player_possessions(
            game_id=game_id_list[0],
            player_class=player_class,
            df_possession=df_possession_region,
            df_game_stats=df_game_stats
        )

        # update possession probability
        ppp.update_possession_prob(
            player_class=player_class,
            df_possession=df_possession,
            game_id=None
        )

        # update action probabilities
        ppp.get_action_prob_matrix(
            player_class=player_class,
            df_possession=df_possession
        )

        # update shooting_prob
        ppp.get_shooting_prob(
            player_class=player_class,
            df_game_stats=df_game_stats
        )

        # update region_shooting_prob
        ppp.get_regional_shooting_prob(
            player_class=player_class,
            df_possession=df_possession
        )

        # update season steals/blocks per game
        pdh.update_traditional_nba_stats(
            player_class=player_class,
            season='2015-16',
            season_type='Regular Season'
        )

    df_possession_defender_team1 = pdh.get_df_possession_defender(
        offense_players_dict=team2_class_dict,
        df_possession_region=df_possession_region,
        df_raw_position_region=df_raw_position_region,
        defender_team_id=team1_id
    )
    df_possession_defender_team2 = pdh.get_df_possession_defender(
        offense_players_dict=team1_class_dict,
        df_possession_region=df_possession_region,
        df_raw_position_region=df_raw_position_region,
        defender_team_id=team2_id
    )

    # Update team1 defence data
    for player_class in team1_class_dict.values():
        # update possession outcome when defending
        pdh.poss_result_on_defense(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team1,
            game_id=None
        )

        pdh.poss_result_on_defense_reg(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team1,
            game_id=None
        )

        pdh.get_def_off_region_matrix(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team1,
            game_id=None,
        )
    # Update team2 defense data
    for player_class in team2_class_dict.values():
        # update possession outcome when defending
        pdh.poss_result_on_defense(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team2,
            game_id=None
        )

        pdh.poss_result_on_defense_reg(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team2,
            game_id=None
        )

        pdh.get_def_off_region_matrix(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team2,
            game_id=None,
        )

    start_play = True
    player_action = None
    shooting_side = 'right'
    score = 0

    for i in range(10):
        player_action, start_play, score = spp.sim_offense_play(
            players_offense_dict=team1_class_dict,
            players_defense_dict=team2_class_dict,
            shooting_side=shooting_side,
            start_play=start_play,
            player_action=player_action,
            score=score
        )

        print i
        print 'action: ', player_action
        print 'score: ', score

        for player_class in team1_class_dict.values():
            print player_class.name
            print 'region', player_class.court_region
            print 'possession', player_class.has_possession
            print 'passes', player_class.passes
            print 'shot_attempts', player_class.shot_attempts
            print 'shots_made', player_class.shots_made
            print 'turnovers', player_class.turnovers
            print 'total_points', player_class.total_points
            print ""

    sim_coord_dict = spp.create_sim_coord_dict(
        players_offense_dict=team1_class_dict,
        num_sim=100)

    players_no_ball_dict = spp.get_player_dict_no_ball(
        players_offense_dict=team1_class_dict
    )

    # to re-do the simulation we reset the parameters
    # player_class_reset(team1_id_dict)
