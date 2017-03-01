import matplotlib.pyplot as plt
import numpy as np
import triple_triple.simulate_player_positions as spp
from triple_triple.full_court import draw_court

#TODO: Fix player_color_dict having colors in argument
# TODO: Fix color list in bar graph
# TODO: Real time plotting: http://stackoverflow.com/questions/11874767/real-time-plotting-in-while-loop-with-matplotlib
# TODO: Multiple color bars http://stackoverflow.com/questions/22128166/two-different-color-colormaps-in-the-same-imshow-matplotlib


def generate_pixel_points(old_list, num_pixel):
    new_list = []
    pixel = num_pixel - 1

    for i in range(len(old_list) - 1):
        width = (old_list[i + 1] - old_list[i]) / \
            float(pixel)

        for j in range(pixel):
            new_list.append(old_list[i] + j * width)

    # add back last coordinate
    new_list.append(old_list[-1])
    return new_list


def create_pixel_coord_dict(sim_coord_dict, num_pixel):
    pixel_sim_coord_dict = {}
    for player, coord in sim_coord_dict.items():
        x, y = zip(*coord)
        pixel_sim_coord_dict[player] = \
            (generate_pixel_points(x, num_pixel=50),
             generate_pixel_points(y, num_pixel=50))

    return pixel_sim_coord_dict


def plot_jersey_numbers(ax, players_dict):
    for player_class in players_dict.values():
        ax.annotate(
            s=player_class.jersey,
            xy=player_class.court_coord,
            xytext=(player_class.court_coord[0] - 0.5,
                    player_class.court_coord[1] - 0.5)
        )


def create_player_color_dict(coord_dict):
    color_map_list = [plt.cm.Blues, plt.cm.Greens, plt.cm.Oranges,
                      plt.cm.Purples, plt.cm.Reds, plt.cm.autumn]
    player_color_dict = {}
    i = 0
    for player in coord_dict.keys():
        player_color_dict[player] = color_map_list[i]
        i += 1

    return player_color_dict


def plot_color_bars(ax, color_bar_dict, players_offense_dict):
    for player, cbar in color_bar_dict.items():
        cbar.set_label(players_offense_dict[player].name, labelpad=-30)
        cbar.ax.invert_xaxis()
        

def plot_play_simulation(
    players_offense_dict,
    player_defense_dict={},
    num_sim=5,
    num_pixel=50,
    title_text='Team'
):

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    ax.set_xlim([-2, 97])
    ax.set_ylim([0, 50])

    # simulate the play
    sim_coord_dict = spp.create_sim_coord_dict(players_offense_dict, num_sim)

    # get color dict, time coord and pixeled coord
    players_color_dict = create_player_color_dict(sim_coord_dict)
    time_coord = generate_pixel_points(np.arange(num_sim), num_pixel)
    pixel_sim_coord_dict = create_pixel_coord_dict(sim_coord_dict, num_pixel)

    # construct color_bar dict
    color_bar_dict = {}
    for player, coord in pixel_sim_coord_dict.items():
        plt.scatter(
            x=coord[0],
            y=coord[1],
            c=time_coord,
            cmap=players_color_dict[player],
            s=200,
            zorder=1
        )
        color_bar_dict[player] = plt.colorbar(
            format='%.2f',
            orientation="horizontal",
            fraction=0.046,
            pad=0.04,
            shrink=0.38
        )

    # plot jersey number
    plot_jersey_numbers(ax=ax, players_dict=players_offense_dict)

    # plot cbars
    plot_color_bars(ax, color_bar_dict, players_offense_dict)

    ax.set_title(title_text + ' simulated court movement')
    fig.savefig('player_sim_movement.png')
    plt.show()


def plot_outcomes_bar_graph(players_offense_dict, color_list):
    N = 4 # (passes, shot_attempts, shots_made, turnovers)
    ind = np.arange(N)
    width = 0.18
    fig, ax = plt.subplots()
    i = 0

    legend_ax_list = []
    legend_name_list = []

    for player_class in players_offense_dict.values():
        player_outcome = [
            player_class.passes,
            player_class.shot_attempts,
            player_class.shots_made,
            player_class.turnovers
        ]
        player = ax.bar(ind + i * width, player_outcome, width, color=color_list[i])
        legend_ax_list.append(player[0])
        legend_name_list.append(player_class.name)

        # increment i
        i += 1

    ax.set_ylabel('Totals')
    ax.set_title('Player outcomes after 100 simulations')
    ax.set_xticks(ind + 2.2 * width)
    ax.set_xticklabels((
        'passes', 'shot attempts', 'shots made', 'turnovers'))

    ax.legend(legend_ax_list, legend_name_list)
    fig.savefig('sim_outcome_results.png')
    plt.show()
