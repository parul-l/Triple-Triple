from bokeh.embed import components
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from triple_triple.config import IMG_DIR
from triple_triple.plot.full_court import (
    draw_court,
    draw_court_bokeh
)

# This file has two methods of colour blocking the court:
# 1. Using mathplotlib
# 2. Using Bokeh

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
ax.set_xlim([0, 94])
ax.set_ylim([0, 50])


def region_block_court(ax=ax):
    # PAINT
    ax.add_patch(patches.Rectangle(
        xy=(75, 19),
        width=19,
        height=12,
        facecolor='#1e9abe',
        alpha=0.4,
        edgecolor='none',
        label='paint')
    )

    # BACK COURT
    ax.add_patch(patches.Rectangle(
        xy=(0, 0),
        width=47,
        height=50,
        facecolor='#e82e15',
        alpha=0.6,
        edgecolor='none',
        label='back court')
    )

    # KEY
    ax.add_patch(patches.Wedge(
        center=(75, 25),
        r=6,
        theta1=0,
        theta2=360,
        ec='none',
        facecolor='#04d18d',
        alpha=0.6,
        edgecolor='none',
        label='key')
    )

    # MID-RANGE
    ax.add_patch(patches.Rectangle(
        xy=(80, 3),
        width=16,
        height=16,
        facecolor='#601ebe',
        alpha=0.6,
        edgecolor='none')
    )
    ax.add_patch(patches.Rectangle(
        xy=(80, 31),
        width=16,
        height=16,
        facecolor='#601ebe',
        alpha=0.6,
        edgecolor='none',
        label='mid-range')
    )

    # # 3 point circle: (x - 88.75)**2 + (y - 25)**2 = 23.75**2
    # # key circle: (x - 75)**2 + (y - 25)**2 = 6**2

    # top and bottom right arc
    x1 = np.arange(75, 80, 0.01)
    y1 = 19
    y2 = - np.sqrt((23.75)**2 - (x1 - 88.75)**2) + 25
    y3 = np.sqrt((23.75)**2 - (x1 - 88.75)**2) + 25
    y4 = 31
    ax.fill_between(x1, y1, y2, facecolor='#601ebe', alpha=0.6, lw=0)
    ax.fill_between(x1, y3, y4, facecolor='#601ebe', alpha=0.6, lw=0)

    # top and bottom left arc
    x2 = np.arange(69, 75, 0.01)
    y1 = - np.sqrt(6**2 - (x2 - 75)**2) + 25
    y2 = - np.sqrt((23.75)**2 - (x2 - 88.75)**2) + 25
    y3 = np.sqrt((23.75)**2 - (x2 - 88.75)**2) + 25
    y4 = np.sqrt(6**2 - (x2 - 75)**2) + 25
    ax.fill_between(x2, y1, y2, facecolor='#601ebe', alpha=0.6, lw=0)
    ax.fill_between(x2, y3, y4, facecolor='#601ebe', alpha=0.6, lw=0)

    x3 = np.arange(65, 69, 0.01)
    y1 = np.sqrt((23.75)**2 - (x3 - 88.75)**2) + 25
    y2 = - np.sqrt((23.75)**2 - (x3 - 88.75)**2) + 25
    ax.fill_between(x3, y1, y2, facecolor='#601ebe', alpha=0.6, lw=0)

    # PERIMETER
    ax.add_patch(patches.Rectangle(
        xy=(47, 0),
        width=18,
        height=50,
        facecolor='#78ff00',
        alpha=0.4,
        edgecolor='none')
    )
    ax.add_patch(patches.Rectangle(
        xy=(80, 0),
        width=14,
        height=3,
        facecolor='#78ff00',
        alpha=0.4,
        edgecolor='none')
    )
    ax.add_patch(patches.Rectangle(
        xy=(80, 47),
        width=14,
        height=3,
        facecolor='#78ff00',
        alpha=0.4,
        edgecolor='none',
        label='perimeter')
    )

    # arc regions
    x4 = np.arange(65, 80, 0.01)
    y1 = - np.sqrt((23.75)**2 - (x4 - 88.75)**2) + 25
    y2 = 0
    y3 = 50
    y4 = np.sqrt((23.75)**2 - (x4 - 88.75)**2) + 25
    ax.fill_between(x4, y1, y2, facecolor='#78ff00', alpha=0.4, lw=0)
    ax.fill_between(x4, y3, y4, facecolor='#78ff00', alpha=0.4, lw=0)

    plt.legend(loc='upper left')
    filepath = os.path.join(IMG_DIR, 'full_court_region_block.png')
    fig.savefig(filepath)

    plt.show()
    return ax


def label_court_prob(ax, prob_array):
    # reg_to_num = {
    #     'back court': 0,
    #     'mid-range': 1,
    #     'key': 2,
    #     'out of bounds': 3,
    #     'paint': 4,
    #     'perimeter': 5
    # }

    # back court
    ax.text(30, 25, str(prob_array[0]) + '%', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    # mid-range
    ax.text(80, 37, str(prob_array[1]) + '%', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    # key
    ax.text(70, 25, str(prob_array[2]) + '%', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    # paint
    ax.text(82, 25, str(prob_array[4]) + '%', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    # perimeter
    ax.text(53, 25, str(prob_array[5]) + '%', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

    return ax

#####################
# USING BOKEH #
#####################
# 3 point circle: (x - 88.75)**2 + (y - 25)**2 = 23.75**2
# key circle: (x - 75)**2 + (y - 25)**2 = 6**2

# 3 point circle: (x - 88.75)**2 + (y - 25)**2 = 23.75**2
# key circle: (x - 75)**2 + (y - 25)**2 = 6**2


def three_point_bottom_arc(x):
    return - np.sqrt((23.75)**2 - (x - 88.75)**2) + 25


def three_point_top_arc(x):
    return np.sqrt((23.75)**2 - (x - 88.75)**2) + 25


def key_bottom_arc(x):
    return - np.sqrt(6**2 - (x - 75)**2) + 25


def key_top_arc(x):
    return np.sqrt(6**2 - (x - 75)**2) + 25


def region_draw_court_bokeh(line_width=2):
    plot = draw_court_bokeh()

    # PAINT
    plot.quad(
        left=[75], right=[94], bottom=[19], top=[31],
        fill_color='#1e9abe', alpha=0.4,
        line_alpha=0,
        legend='Paint'
    )

    # BACK COURT
    plot.quad(
        left=[0], right=[47], bottom=[0], top=[50],
        fill_color='#98FB98', alpha=0.6,
        line_alpha=0,
        legend='Back Court'
    )

    # TOP OF KEY
    plot.wedge(
        x=[75], y=[25],
        radius=6, start_angle=90, end_angle=270, color='#FFA07A', alpha=0.6,
        start_angle_units='deg',
        end_angle_units='deg',
        line_alpha=0,
        legend='Top of Key'
    )

    # MID-RANGE
    plot.quad(
        left=[80], right=[94], bottom=[3], top=[19],
        fill_color='#9370DB', alpha=0.4, line_alpha=0
    )
    plot.quad(
        left=[80], right=[94], bottom=[31], top=[47],
        fill_color='#9370DB', alpha=0.4, line_alpha=0,
        legend='Mid-Range'
    )
    # BOTTOM1: three_point_bottom_arc
    x_bottom = np.arange(75, 80, 0.01)
    x_top = x_bottom[::-1]
    yb_bottom = np.apply_along_axis(three_point_bottom_arc, axis=0, arr=x_bottom)
    yb_top = np.tile(19, len(x_top))

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yb_bottom, yb_top), axis=0),
        color='#9370DB', fill_alpha=0.4,
        line_alpha=0
    )
    # TOP1: three_point_top_arc
    yt_bottom = np.tile(31, len(x_top))
    yt_top = np.apply_along_axis(three_point_top_arc, axis=0, arr=x_top)

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yt_bottom, yt_top), axis=0),
        color='#9370DB', fill_alpha=0.4,
        line_alpha=0
    )

    # BOTTOM2:
    x_bottom = np.arange(69, 75, 0.01)
    x_top = x_bottom[::-1]
    yb_bottom = np.apply_along_axis(three_point_bottom_arc, axis=0, arr=x_bottom)
    yb_top = np.apply_along_axis(key_bottom_arc, axis=0, arr=x_top)

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yb_bottom, yb_top), axis=0),
        color='#9370DB', fill_alpha=0.4,
        line_alpha=0
    )

    # TOP2
    yt_bottom = np.apply_along_axis(key_top_arc, axis=0, arr=x_bottom)
    yt_top = np.apply_along_axis(three_point_top_arc, axis=0, arr=x_top)

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yt_bottom, yt_top), axis=0),
        color='#9370DB', fill_alpha=0.4,
        line_alpha=0
    )

    # LAST PIECE:
    x_bottom = np.arange(65, 69, 0.01)
    x_top = x_bottom[::-1]
    yb_bottom = np.apply_along_axis(three_point_bottom_arc, axis=0, arr=x_bottom)
    yb_top = np.apply_along_axis(three_point_top_arc, axis=0, arr=x_top)

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yb_bottom, yb_top), axis=0),
        color='#9370DB', fill_alpha=0.4,
        line_alpha=0
    )

    # PERIMETER
    plot.quad(
        left=[47, 80, 80], right=[65, 94, 94], bottom=[0, 0, 47], top=[50, 3, 50],
        fill_color='#FFFF00', alpha=0.4,
        line_alpha=0,
        legend='Perimeter'
    )

    # PERIMETER ARCS - BOTTOM
    x_bottom = np.arange(65, 80, 0.01)
    x_top = x_bottom[::-1]
    yb_bottom = np.tile(0, len(x_bottom))
    yb_top = np.apply_along_axis(three_point_bottom_arc, axis=0, arr=x_top)

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yb_bottom, yb_top), axis=0),
        color='#FFFF00', fill_alpha=0.4,
        line_alpha=0
    )
    # PERIMETER ARCS - TOP
    x_bottom = np.arange(65, 80, 0.01)
    x_top = x_bottom[::-1]
    yt_bottom = np.apply_along_axis(three_point_top_arc, axis=0, arr=x_bottom)
    yt_top = np.tile(50, len(x_top))

    plot.patch(
        x=np.concatenate((x_bottom, x_top), axis=0),
        y=np.concatenate((yt_bottom, yt_top), axis=0),
        color='#FFFF00', fill_alpha=0.4,
        line_alpha=0
    )

    plot.legend.orientation = 'horizontal'
    plot.legend.location = "bottom_center"

    script, div = components(plot)

    return script, div
