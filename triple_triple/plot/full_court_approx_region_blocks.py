import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from triple_triple.config import IMG_DIR
from triple_triple.plot.full_court import draw_court


fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
ax.set_xlim([-2, 96])
ax.set_ylim([0, 50])


def approx_region_block_court(ax=ax):
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
        theta1=90,
        theta2=270,
        ec='none',
        facecolor='#04d18d',
        alpha=0.6,
        edgecolor='none',
        label='key')
    )

    # MID-RANGE
    ax.add_patch(patches.Rectangle(
        xy=(80, 3),
        width=14,
        height=16,
        facecolor='#601ebe',
        alpha=0.6,
        edgecolor='none')
    )
    ax.add_patch(patches.Rectangle(
        xy=(80, 31),
        width=14,
        height=16,
        facecolor='#601ebe',
        alpha=0.6,
        edgecolor='none',
        label='mid-range')
    )

    # # 3 point circle: (x - 88.75)**2 + (y - 25)**2 = 23.75**2
    # # key circle: (x - 75)**2 + (y - 25)**2 = 6**2

    x3 = np.arange(65, 69, 0.01)
    y1 = np.sqrt((23.75)**2 - (x3 - 88.75)**2) + 25
    y2 = - np.sqrt((23.75)**2 - (x3 - 88.75)**2) + 25
    ax.fill_between(x3, y1, y2, facecolor='#601ebe', alpha=0.6, lw=0)

    # PERIMETER
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

    # triangle regions
    x1 = np.arange(47, 80, 0.01)
    y1 = 0
    y2 = - (25 / 33.) * x1 + (25 / 33.) * 80
    y3 = (25 / 33.) * x1 + (25 - (25 / 33.) * 47)
    y4 = 50
    ax.fill_between(x1, y1, y2, facecolor='#78ff00', alpha=0.4, lw=0)
    ax.fill_between(x1, y3, y4, facecolor='#78ff00', alpha=0.4, lw=0)

    plt.legend(loc='upper left')

    plot_random_generated_points()

    # filepath = os.path.join(IMG_DIR, 'full_court_approx_region_block.png')
    # fig.savefig(filepath)

    # plt.show()
    return ax


def plot_random_generated_points(ax=ax):
    # back court
    ax.scatter([23.5], [25], s=100)

    # mid-range
    ax.scatter([84.5, 84.5, 67], [11, 39, 25], s=100)

    # key
    ax.scatter([72], [25], s=100)

    # paint
    ax.scatter([84.5], [25], s=100)

    # out of bounds
    ax.scatter([96], [25], s=100)

    # perimeter
    ax.scatter([89, 89, 58, 58], [1.5, 48.5, 8.33, 41.67], s=100)

    return ax
