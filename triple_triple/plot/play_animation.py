# RESTRUCTURED:
# TODO: CLEAN THIS UP AND INCORPORATE ONE-PLAYER

import numpy as np
from matplotlib import animation


def get_fixedtime_df(
    period,
    time_start,
    time_end,
    dataframe
):

    return dataframe.query(
        '@time_end <= game_clock <= @time_start and '
        'period == @period')


def team_coord(team_id, df_grouped_value):
    # coord and jersey_number
    x_coord = df_grouped_value.query('team_id==@team_id').x_loc.values
    y_coord = df_grouped_value.query('team_id==@team_id').y_loc.values
    jersey = df_grouped_value.query('team_id==@team_id').player_jersey.values

    return x_coord, y_coord, jersey


def plot_points(ax, x_points, y_points, color):
    return ax.scatter(x_points, y_points, color=color, s=400)


def annotate_points(ax, xx, yy, jersey):
    return [
        ax.annotate(jersey_num, xy=(x - 0.5, y - 0.4))
        for x, y, jersey_num in zip(xx, yy, jersey)
    ]


def update_annotations(annotations, xx, yy):
    for x, y, anno in zip(xx, yy, annotations):
        anno.set_position((x - 0.5, y - 0.4))


def play_animation(
    period,
    time_start,
    time_end,
    fig,
    game_info_dict,
    dataframe
):

    df_fixedtime = get_fixedtime_df(
        period=period,
        time_start=time_start,
        time_end=time_end,
        dataframe=dataframe
    )

    # tuple: (game_clock, shot_clock)
    grouped_fixedtime = df_fixedtime.groupby(
        ['game_clock', 'shot_clock']
    )
    instance_array = grouped_fixedtime.groups.keys()
    instance_array.sort(reverse=True)
    # initial frame
    df_grouped_value = grouped_fixedtime.get_group(instance_array[0])
    # get coordintates
    ax = fig.gca()
    msg_game_clock = 'game clock: ' + str(instance_array[0][0])
    msg_shot_clock = 'shot clock: ' + str(instance_array[0][1])
    msg_ball_height = 'ball height: ' + str(df_grouped_value.moment.iloc[0])

    game_clock_annotations = ax.text(-18, 25, msg_game_clock)
    shot_clock_annotations = ax.text(-18, 20, msg_shot_clock)
    ball_height_annotations = ax.text(-18, 15, msg_ball_height)

    # initialize the frame
    def init():
        game_clock_annotations.set_text('initial')
        shot_clock_annotations.set_text('initial')
        ball_height_annotations.set_text('initial')
        scat_home.set_offsets([])
        scat_away.set_offsets([])
        scat_ball.set_offsets([])

        return scat_home, scat_away, scat_ball, game_clock_annotations, \
            shot_clock_annotations, ball_height_annotations

    # initial player coordinates
    hometeam_id = game_info_dict['hometeam_id']
    visitorteam_id = game_info_dict['visitorteam_id']

    x_home, y_home, jersey_home = team_coord(
        team_id=hometeam_id,
        df_grouped_value=df_grouped_value
    )
    x_away, y_away, jersey_away = team_coord(
        team_id=visitorteam_id,
        df_grouped_value=df_grouped_value
    )

    # initial ball coordinates
    x_ball, y_ball, ball_id = team_coord(
        team_id=-1,
        df_grouped_value=df_grouped_value
    )

    # plot the initial point
    scat_home = plot_points(ax, x_home, y_home, color='blue')
    scat_away = plot_points(ax, x_away, y_away, color='red')
    scat_ball = plot_points(ax, x_ball, y_ball, color='black')

    # label the coordinates
    home_annotations = annotate_points(ax, x_home, y_home, jersey_home)
    away_annotations = annotate_points(ax, x_away, y_away, jersey_away)

    def update(frame_number):
        df_grouped_value = grouped_fixedtime\
            .get_group(instance_array[frame_number])

        x_home, y_home, jeresy_home = team_coord(
            team_id=hometeam_id, df_grouped_value=df_grouped_value)
        x_away, y_away, jeresy_away = team_coord(
            team_id=visitorteam_id, df_grouped_value=df_grouped_value)
        x_ball, y_ball, ball_id = team_coord(
            team_id=-1, df_grouped_value=df_grouped_value)

        # set_offsets expects N x 2 array
        data_home = np.array([x_home, y_home]).T
        data_away = np.array([x_away, y_away]).T
        scat_home.set_offsets(data_home)
        scat_away.set_offsets(data_away)
        scat_ball.set_offsets((x_ball, y_ball))

        update_annotations(home_annotations, x_home, y_home)
        update_annotations(away_annotations, x_away, y_away)

        # update game_clock and shot_clock:
        game_clock_annotations.set_text(
            'game clock: ' + str(instance_array[frame_number][0]))
        shot_clock_annotations.set_text(
            'shot clock: ' + str(instance_array[frame_number][1]))
        ball_height_annotations.set_text(
            'ball height: ' + str(df_grouped_value.moment.iloc[0]))

    # number of frames
    no_frame = len(instance_array)

    anim = animation.FuncAnimation(
        fig=fig,
        init_func=init,
        func=update,
        frames=no_frame,
        blit=False,
        interval=10,
        repeat=False
    )

    # anim.save('play.mpeg', fps=10, extra_args=['-vcodec', 'libx264'])

    return anim
