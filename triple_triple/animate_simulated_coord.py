import matplotlib.pyplot as plt
from matplotlib import animation

from triple_triple.full_court import draw_court
from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_pos_dist
)
from triple_triple.player_passing_habits import get_player_court_region_df
from triple_triple.generate_player_positions import (
    get_player_region_prob,
    get_player_simulated_regions,
    # generate_back_court,
    # generate_mid_range,
    # generate_key,
    # generate_out_of_bounds,
    # generate_paint,
    # generate_perimeter,
    # generate_rand_positions,
    get_simulated_coord,
)
from triple_triple.play_animation import (
    playerid_from_name,
    plot_points,
)


def sim_animation(player_sim_coord):
    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)

    def init():
        return scat_player.set_offsets([])

    x_coord, y_coord = zip(*player_sim_coord)

    playerid = playerid_from_name(player_name)
    team = game_id_dict[playerid][2]

    # plot initial points
    if team == hometeam_id:
        color = 'blue'
    elif team == awayteam_id:
        color = 'red'

    # label jersey_number
    anno = ax.annotate(
        game_id_dict[playerid][1],
        xy=(x_coord[0] - 0.5, y_coord[0] - 0.4)
    )

    scat_player = plot_points(ax, x_coord[0], y_coord[0], color=color)

    def update(frame_number):
        scat_player.set_offsets((x_coord[frame_number], y_coord[frame_number]))
        anno.set_position(
            (x_coord[frame_number] - 0.5, y_coord[frame_number] - 0.4)
        )

    no_frame = len(x_coord)

    anim = animation.FuncAnimation(
        fig,
        func=update,
        init_func=init,
        frames=no_frame,
        interval=200,
        blit=False
    )

    return anim

############################
############################

if __name__ == '__main__':
    game_id_dict = get_game_id_dict()
    df_pos_dist = get_df_pos_dist()
    df_pos_dist_reg = get_player_court_region_df(df_pos_dist)

    reg_to_num = {
        'bench': 0,
        'back court': 1,
        'mid-range': 2,
        'key': 3,
        'out of bounds': 4,
        'paint': 5,
        'perimeter': 6
    }

    player_name = 'Chris Bosh'
    df_player_region = list(df_pos_dist_reg[player_name].region)
    player_reg_prob = get_player_region_prob(player_name, df_pos_dist_reg)

    player_sim_reg = get_player_simulated_regions(player_reg_prob, num_sim=100)

    player_sim_coord = get_simulated_coord(player_sim_reg, 'left')

    anim = sim_animation(player_sim_coord)
    plt.show()
    plt.ioff()
