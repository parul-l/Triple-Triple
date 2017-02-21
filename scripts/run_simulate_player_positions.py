import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp
import triple_triple.player_possession_habits as pph

from triple_triple.class_player import (
    create_player_class_instance,
    player_class_reset
)

from triple_triple.startup_data import (
    get_df_raw_position_region,
    get_game_player_dict,
    get_df_play_by_play
)
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play

df_raw_position_region = get_df_raw_position_region()
game_player_dict = get_game_player_dict()
df_play_by_play = get_df_play_by_play()
df_game_stats = parse_df_play_by_play(df_play_by_play)


if __name__ == '__main__':
    player_id_list = [-1, 2547, 2548, 2736, 1626159, 201609]
    game_id_list = [21500568]

    df_possession = pph.get_possession_df(
        dataframe=df_raw_position_region,
        len_poss=10
    )

    reg_to_num = {
        'back court': 0,
        'mid-range': 1,
        'key': 2,
        'out of bounds': 3,
        'paint': 4,
        'perimeter': 5
    }

    players_offense_dict = create_player_class_instance(
        player_list=player_id_list,
        game_player_dict=game_player_dict,
    )

    # remove ball to update probabilities
    players_no_ball_dict = spp.get_player_dict_no_ball(
        players_offense_dict=players_offense_dict
    )

    for player_class in players_no_ball_dict.values():
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
            df_possession=df_possession,
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

    start_play = True
    player_action = None
    shooting_side = 'right'

    for i in range(10):
        player_action, start_play, score = spp.sim_offense_play(
            players_offense_dict=players_offense_dict,
            shooting_side=shooting_side,
            start_play=start_play,
            player_action=player_action
        )

        print i
        print 'action: ', player_action
        print 'score: ', score

        for player_class in players_offense_dict.values():
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
        players_offense_dict=players_offense_dict,
        num_sim=100)

    players_no_ball_dict = spp.get_player_dict_no_ball(
        players_offense_dict=players_offense_dict
    )

    # to re-do the simulation we reset the parameters
    player_class_reset(players_offense_dict)
