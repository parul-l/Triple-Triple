import matplotlib.pyplot as plt
import numpy as np
from triple_triple.full_court import draw_court


def generate_pixel_points(x1, x2, new_coord_list, num_pixel):
    width = (x2 - x1) / float(num_pixel - 1)

    for i in range(num_pixel):
        new_coord_list.append(x1 + i * width)

    return new_coord_list


def plot_player_simulation(sim_coord, player_name):
    x, y = zip(*sim_coord)
    t = np.arange(len(x))

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    ax.set_xlim([0, 94])
    ax.set_ylim([0, 50])

    x_new = []
    y_new = []
    t_new = []

    for i in range(len(x) - 1):
        x_new = generate_pixel_points(x[i], x[i + 1], x_new, num_pixel=50)
        y_new = generate_pixel_points(y[i], y[i + 1], y_new, num_pixel=50)
        t_new = generate_pixel_points(t[i], t[i + 1], t_new, num_pixel=50)

    plt.scatter(x_new, y_new, c=t_new, cmap=plt.cm.Blues, s=200, zorder=1)
    cbar = plt.colorbar(format='%.3f', orientation="horizontal")
    cbar.ax.invert_xaxis()

    ax.set_title(player_name + ' simulated court movement')
    fig.savefig('player_sim_movement.png')
    plt.show()


def plot_play_simulation(players_offense_dict, player_defense_dict, num_sim=10):
    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    ax.set_xlim([0, 94])
    ax.set_ylim([0, 50])
