import triple_triple.player_possession_habits as pph
import triple_triple.prob_player_possessions as ppp
import triple_triple.simulate_player_positions as spp

from triple_triple.team_shooting_side import get_initial_shooting_sides

from triple_triple.player_simulation_plot import plot_player_simulation

from triple_triple.startup_data import (
    get_df_play_by_play,
    get_df_raw_position_data,
    get_game_info_dict
)

df_raw_position_data = get_df_raw_position_data()
df_play_by_play = get_df_play_by_play()
game_info_dict = get_game_info_dict()

initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_raw_position_data, game_info_dict)

if __name__ == '__main__':

    reg_to_num = {
        'back court': 0,
        'mid-range': 1,
        'key': 2,
        'out of bounds': 3,
        'paint': 4,
        'perimeter': 5
    }

    player_id_list = [2547]

    df_player = df_raw_position_data.query('player_id==@player_id_list[0]')
    df_raw_position_region = pph.add_regions_to_df(df_player, initial_shooting_side)

    movement_prob = ppp.get_movement_prob_matrix(player_id_list, df_raw_position_region)

    # choose player to simulate
    sim_reg = spp.get_player_sim_reg(cond_prob_movement=movement_prob[2547], num_sim=300, num_regions=6)

    sim_coord = spp.get_simulated_coord(player_sim_reg=sim_reg, shooting_side='right')

    plot_player_simulation(sim_coord[:10], df_raw_position_data)
