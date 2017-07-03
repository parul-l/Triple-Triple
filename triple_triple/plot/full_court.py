import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as mc
from bokeh.plotting import figure, output_file

# There are two plots for the court: one using 
# matplotlib and the other using bokeh


def draw_court(ax=None, linewidth=2, color='black'):
    if ax is None:
        ax = plt.gca()
    # set full court dimension
    ax.add_patch(patches.Rectangle(
        (0, 0),             # (x, y)
        94,                 # width
        50,                 # length
        fill=False)
    )
    # half court line segments
    lines_hc = [
        [(0, 3), (14, 3)],      # 3 point sideline
        [(0, 47), (14, 47)],    # 3 point sideline
        [(0, 19), (19, 19)],    # key
        [(0, 31), (19, 31)],    # key
        [(4, 22), (4, 28)],     # backboard
        [(4, 25), (4.5, 25)],   # rim line
        [(47, 0), (47, 50)]
    ]
    # other side half court line segments
    lines_other = [
        [(94, 3), (80, 3)],     # 3 point sideline
        [(94, 47), (80, 47)],   # 3 point sideline
        [(94, 19), (75, 19)],   # key
        [(94, 31), (75, 31)],   # key
        [(90, 22), (90, 28)],   # backboard
        [(90, 25), (89.5, 25)], # rim line
        [(47, 0), (47, 50)]
    ]
    lc = mc.LineCollection(lines_hc, color='black', linewidths=2)
    lc_other = mc.LineCollection(lines_other, color='black', linewidths=2)
    ax.add_collection(lc_other)
    ax.add_collection(lc)

    # half court rectangles
    ax.add_patch(patches.Rectangle((0, 17), 19, 16, fill=False))
    ax.add_patch(patches.Rectangle((75, 17), 19, 16, fill=False))

    # little hash marks (2in wide x 6in height)
    for p in [
        patches.Rectangle((7, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((8, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((11, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((14, 16.5), 0.17, 0.5, color='black'),

        patches.Rectangle((89, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((88, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((85, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((82, 16.5), 0.17, 0.5, color='black'),
        ###################
        # other side
        ###################
        patches.Rectangle((7, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((8, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((11, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((14, 33), 0.17, 0.5, color='black'),

        patches.Rectangle((89, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((88, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((85, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((82, 33), 0.17, 0.5, color='black'),
        #####################
        # marks on sidelines
        #####################
        patches.Rectangle((28, 0), 0.17, 3, color='black'),
        patches.Rectangle((28, 47), 0.17, 3, color='black'),

        patches.Rectangle((66, 0), 0.17, 3, color='black'),
        patches.Rectangle((66, 47), 0.17, 3, color='black'),
    ]:
        ax.add_patch(p)

    # half court arcs
    for p in [
        # center court
        patches.Arc((47, 25), 12, 12, theta1=0, theta2=360,
                    linewidth=2, fill=False),
        # center court
        patches.Arc((47, 25), 4, 4, theta1=0, theta2=360,
                    linewidth=2, fill=False),
        # top of the key
        patches.Arc((19, 25), 12, 12, theta1=270, theta2=90.0,
                    fill=False),

        patches.Arc((75, 25), 12, 12, theta1=90, theta2=270.0,
                    fill=False),

        patches.Arc((19, 25), 12, 12, theta1=90.0, theta2=270.0,
                    linestyle='dashed'),
        patches.Arc((75, 25), 12, 12, theta1=270.0, theta2=90.0,
                    linestyle='dashed'),

        # 3 point line
        patches.Arc((5.25, 25), 47.5, 47.5, theta1=-68.38, theta2=68.38,
                    linewidth=2),
        patches.Arc((88.75, 25), 47.5, 47.5, theta1=111.62, theta2=248.38,
                    linewidth=2),
        # restricted area
        patches.Arc((5.25, 25), 8, 8, theta1=270, theta2=90.0,
                    fill=False),
        patches.Arc((88.75, 25), 8, 8, theta1=90, theta2=270.0,
                    fill=False),

        # hoop
        patches.Arc((5.25, 25), 1.5, 1.5, theta1=0.0, theta2=360.0,
                    fill=False),
        patches.Arc((88.75, 25), 1.5, 1.5, theta1=0.0, theta2=360.0,
                    fill=False),

    ]:
        ax.add_patch(p)
    return ax


def draw_court_bokeh(line_color='black', line_width=2):
    plot = figure(width=650, height=350)
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    # set full court dimension
    plot.quad(
        bottom=[0], top=[50], left=[0], right=[94],
        fill_color=None, line_color=line_color
    )

    # half court line segments left
    lines_hc_left = [
        [(0, 3), (14, 3)],      # 3 point sideline
        [(0, 47), (14, 47)],    # 3 point sideline
        [(0, 19), (19, 19)],    # key
        [(0, 31), (19, 31)],    # key
        [(4, 22), (4, 28)],     # backboard
        [(4, 25), (4.5, 25)],   # rim line
        [(47, 0), (47, 50)]
    ]

    lines_hc_right = [
        [(94, 3), (80, 3)],     # 3 point sideline
        [(94, 47), (80, 47)],   # 3 point sideline
        [(94, 19), (75, 19)],   # key
        [(94, 31), (75, 31)],   # key
        [(90, 22), (90, 28)],   # backboard
        [(90, 25), (89.5, 25)], # rim line
        [(47, 0), (47, 50)]
    ]

    plot.line([4, 4], [22, 28])

    for pair in lines_hc_left + lines_hc_right:
        x, y = zip(*pair)
        plot.line(x, y, line_color=line_color)

    # half_court rectangles
    plot.quad(
        bottom=[17, 17], top=[33, 33], left=[0, 75], right=[19, 94],
        fill_color=None, line_color=line_color
    )

    # little hash marks bottom (2in wide x 6in height)
    b_bottom = [16.5] * 8
    b_left = [7, 8, 11, 14, 89, 88, 85, 82]
    b_right = [x + 0.17 for x in b_left]
    b_top = [x + 0.5 for x in b_bottom]

    # little hash marks top (2in wide x 6in height)
    t_bottom = [33] * 8
    t_left = [7, 8, 11, 14, 89, 88, 85, 82]
    t_right = [x + 0.17 for x in t_left]
    t_top = [x + 0.5 for x in t_bottom]

    plot.quad(
        bottom=b_bottom, left=b_left, right=b_right, top=b_top,
        fill_color='black', line_color=line_color
    )
    plot.quad(
        bottom=t_bottom, left=t_left, right=t_right, top=t_top,
        fill_color='black', line_color=line_color
    )

    # marks on sidelines
    s_bottom = [0, 47, 0, 47]
    s_left = [28, 28, 66, 66]
    s_right = [x + 0.17 for x in s_left]
    s_top = [x + 3 for x in s_bottom]

    plot.quad(
        bottom=s_bottom, left=s_left, right=s_right, top=s_top,
        fill_color='black', line_color=line_color
    )

    # court_arcs:
    center = [
        [47, 25], [47, 25],                     # center court
        [19, 25], [75, 25], [19, 25], [75, 25], # top key
        [5.25, 25], [88.75, 25],                # 3 point line
        [5.25, 25], [88.75, 25],                # restricted area
        [5.25, 25], [88.75, 25]                 # hoop
    ]
    radius = [6, 2, 6, 6, 6, 6, 23.75, 23.75, 4, 4, 0.75, 0.75]
    start_angle = [0, 0, 270, 90, 90, 270, -68.38, 111.62, 270, 90, 0, 0]
    end_angle = [360, 360, 90, 270, 270, 90, 68.38, 248.38, 90, 270, 360, 360]
    line_dash = ['solid'] * 4 + ['dashed'] * 2 + ['solid'] * 6

    arc_params = {
        'center': center,
        'radius': radius,
        'start_angle': start_angle,
        'end_angle': end_angle,
        'line_dash': line_dash,
    }
    num_arcs = len(center)
    for i in range(num_arcs):
        plot.arc(
            x=arc_params['center'][i][0],
            y=arc_params['center'][i][1],
            radius=arc_params['radius'][i],
            start_angle=arc_params['start_angle'][i],
            end_angle=arc_params['end_angle'][i],
            line_dash=arc_params['line_dash'][i],
            line_color=line_color,
            start_angle_units='deg',
            end_angle_units='deg'
        )

    output_file('fullcourt.html')

    return plot
