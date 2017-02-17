import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from triple_triple.config import IMG_DIR
from triple_triple.full_court import draw_court


fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
ax.set_xlim([0, 94])
ax.set_ylim([0, 50])


def region_block_court(ax=ax):
    # PAINT

    ax.add_patch(patches.Rectangle((75, 19), 19, 12, facecolor='#1e9abe', alpha=0.4, edgecolor='none', label='paint'))

    # BACK COURT
    ax.add_patch(patches.Rectangle((0, 0), 47, 50, facecolor='#e82e15', alpha=0.6, edgecolor='none', label='back court'))

    # KEY
    ax.add_patch(patches.Wedge((75, 25), 6, theta1=0, theta2=360, ec='none', facecolor='#04d18d', alpha=0.6, edgecolor='none', label='key'))

    # MID-RANGE
    ax.add_patch(patches.Rectangle((80, 3), 16, 16, facecolor='#601ebe', alpha=0.6, edgecolor='none'))
    ax.add_patch(patches.Rectangle((80, 31), 16, 16, facecolor='#601ebe', alpha=0.6, edgecolor='none', label='mid-range'))

    # 3 point circle: (x - 88.75)**2 + (y - 25)**2 = 23.75**2
    # key circle: (x - 75)**2 + (y - 25)**2 = 6**2

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
    y5 = - np.sqrt(6**2 - (x2 - 75)**2) + 25
    y6 = - np.sqrt((23.75)**2 - (x2 - 88.75)**2) + 25
    y7 = np.sqrt((23.75)**2 - (x2 - 88.75)**2) + 25
    y8 = np.sqrt(6**2 - (x2 - 75)**2) + 25
    ax.fill_between(x2, y5, y6, facecolor='#601ebe', alpha=0.6, lw=0)
    ax.fill_between(x2, y7, y8, facecolor='#601ebe', alpha=0.6, lw=0)

    x3 = np.arange(65, 69, 0.01)
    y9 = np.sqrt((23.75)**2 - (x3 - 88.75)**2) + 25
    y10 = - np.sqrt((23.75)**2 - (x3 - 88.75)**2) + 25
    ax.fill_between(x3, y9, y10, facecolor='#601ebe', alpha=0.6, lw=0)

    # PERIMETER
    ax.add_patch(patches.Rectangle((47, 0), 18, 50, facecolor='#78ff00', alpha=0.4, edgecolor='none'))
    ax.add_patch(patches.Rectangle((80, 0), 14, 3, facecolor='#78ff00', alpha=0.4, edgecolor='none'))
    ax.add_patch(patches.Rectangle((80, 47), 14, 3, facecolor='#78ff00', alpha=0.4, edgecolor='none', label='perimeter'))

    # arc regions
    x4 = np.arange(65, 80, 0.01)
    y11 = - np.sqrt((23.75)**2 - (x4 - 88.75)**2) + 25
    y12 = np.sqrt((23.75)**2 - (x4 - 88.75)**2) + 25
    ax.fill_between(x4, y11, 0, facecolor='#78ff00', alpha=0.4, lw=0)
    ax.fill_between(x4, 50, y12, facecolor='#78ff00', alpha=0.4, lw=0)

    plt.legend(loc='upper left')
    filepath = os.path.join(IMG_DIR, 'full_court_region_block.png')
    fig.savefig(filepath)
    # plt.show()
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
