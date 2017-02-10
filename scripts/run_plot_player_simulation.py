import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp

from triple_triple.class_player import create_player_class_instance
from triple_triple.plot_player_simulation import plot_player_simulation

from triple_triple.startup_data import (
    get_df_raw_position_region,
    get_game_player_dict
)

df_raw_position_region = get_df_raw_position_region()
game_player_dict = get_game_player_dict()


if __name__ == '__main__':

    reg_to_num = {
        'back court': 0,
        'mid-range': 1,
        'key': 2,
        'out of bounds': 3,
        'paint': 4,
        'perimeter': 5
    }

    player_id_list = [2547, 2548]
    game_id_list = [21500568]
    player_classes_dict = create_player_class_instance(
        player_list=player_id_list,
        game_player_dict=game_player_dict,
    )

    for player in player_id_list:
        ppp.update_movement_prob_matrix(
            player_class=player_classes_dict['_' + str(player)],
            game_id=game_id_list[0],
            game_player_dict=game_player_dict,
            df_raw_position_region=df_raw_position_region,
            player_possession=False,
            team_on_offense=True,
            team_on_defense=False,
        )

    # choose player to simulate
    sim_reg = spp.get_player_sim_reg(cond_prob_movement=movement_prob[2547], num_sim=300, num_regions=6)

    sim_coord = spp.get_simulated_coord(player_sim_reg=sim_reg, shooting_side='right')

    plot_player_simulation(sim_coord[:8], df_raw_position_region, 'Chris Bosh')
