import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from triple_triple.plot.full_court import draw_court
from triple_triple.startup_data import get_df_raw_position_data

df_raw_position_data = get_df_raw_position_data()

if __name__ == '__main__':
    game_id_list = [21500568]
    player_id = 201939
    team_id = 1610612744

    # get player locations when his team has ball
    df_player = df_raw_position_data.query('team_id==@team_id and dist_to_ball < 2').query('player_id==@player_id')

    x = df_player.x_loc.values
    y = df_player.y_loc.values

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    ax.set_xlim([0, 94])
    ax.set_ylim([0, 50])

    x_edges = np.arange(0, 95.5, 5)
    y_edges = np.arange(0, 50.5, 5)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=[x_edges, y_edges])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)

    im = ax.imshow(heatmap.T / heatmap.sum(), extent=extent, origin='lower', cmap='viridis')
    fig.colorbar(im, cax=cax, orientation='vertical')
    ax.set_title('Stephen Curry court region proportion in \n' 'Miami Heat vs. Golden State Warriors on Jan 11, 2016')

    fig.savefig('player_region_prob_heatmap.png')

    plt.show()
