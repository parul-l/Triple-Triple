import numpy as np
import matplotlib.pyplot as plt

from triple_triple.data_generators.player_game_stats_data import (
    player_game_stats_nba
)


def plot_player_game_info(player_name, df_player_impact, df_pos_dist):

    player_game_stats = player_game_stats_nba(player_name, df_player_impact)

    df_player = df_pos_dist[(df_pos_dist['closest_player'].values) == player_name]
    # number of total touches. Assuming each touch is about 3 seconds
    # data given 25 frames per second
    touches = len(df_player) / 75.
    shot_attempt = len(player_game_stats[5])
    rebound_count = len(player_game_stats[4])
    foul_count = len(player_game_stats[2])
    free_throw_attempt = len(player_game_stats[3])
    blocks = len(player_game_stats[1])
    turnovers = len(player_game_stats[7])

    passes = touches - shot_attempt - free_throw_attempt - rebound_count - \
        foul_count - blocks - turnovers

    ##################################
    # Histogram plot of percentages
    ##################################
    shot_perc = shot_attempt / touches
    reb_perc = rebound_count / touches
    foul_perc = foul_count / touches
    free_throw_perc = free_throw_attempt / touches
    blocks_perc = blocks / touches
    turnovers_perc = turnovers / touches
    passes_perc = passes / touches

    data_plot = [
        shot_perc,
        reb_perc,
        foul_perc,
        free_throw_perc,
        blocks_perc,
        turnovers_perc,
        passes_perc
    ]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    N = len(data_plot)

    # x location of bars, and their width
    ind = np.arange(N)
    width = 0.35
    # d = ax.bar(ind, data_plot, width, color='red')

    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylim(0, 0.5)
    ax.set_ylabel('Fraction of Touches')
    ax.set_title(player_name + ' Ball Touch Distribution (@ GSW) \n January 11,2016')
    xTickMarks = [
        'Shot Attempts',
        'Rebounds',
        'Fouls',
        'Free Throws',
        'Blocks',
        'Turnovers',
        'Passes'
    ]
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)

    # fig.savefig('player_touches.png')
    plt.show()

    return "Touches=" + str(touches) + \
           " ShotAttempts=" + str(shot_attempt) + \
           " Rebounds=" + str(rebound_count) + \
           " FoulCount=" + str(foul_count) + \
           " FreeThrowAttempts=" + str(free_throw_attempt) + \
           " Blocks=" + str(blocks) + \
           " Turnovers=" + str(turnovers) + \
           " Passes=" + str(passes)
