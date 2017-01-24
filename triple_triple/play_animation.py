# RESTRUCTURED:
# TODO: CLEAN THIS UP AND INCORPORATE ONE-PLAYER 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from triple_triple.full_court import draw_court
from triple_triple.startup_data import (
    get_game_info_dict,
    get_df_raw_position_data,
)

game_info_dict = get_game_info_dict()
df_raw_position_data = get_df_raw_position_data()


def fixedtime_df(period, time_start, time_end, dataframe=df_raw_position_data):
    # return dataframe.query('@time_end <= game_clock <= @time_start and '
    #                       ' period == @period')
    return dataframe[
        (dataframe.game_clock.values <= time_start) &
        (dataframe.game_clock.values >= time_end) &
        (dataframe.period.values == period)
    ]


def team_coord(idx_num, team_id, dataframe):
    grouped_fixedtime = dataframe.groupby(['game_clock', 'shot_clock'])
    instance_array = grouped_fixedtime.groups.keys()

    # group info at ind = idx_num:
    group_info = grouped_fixedtime.get_group(instance_array[idx_num])

    # coord and jersey_number
    x_coord = group_info.query('team_id==@team_id').x_loc.values
    y_coord = group_info.query('team_id==@team_id').y_loc.values
    jersey = group_info.query('team_id==@team_id').player_jersey.values

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


def play_animation(period, time_start, time_end, fig, game_info_dict=game_info_dict, dataframe=df_raw_position_data):
    df_fixedtime = fixedtime_df(
        period=period,
        time_start=time_start,
        time_end=time_end
    )

    # tuple: (game_clock, shot_clock)
    grouped_fixedtime = df_fixedtime.groupby(['game_clock', 'shot_clock'])
    instance_array = grouped_fixedtime.groups.keys()
    instance_array.sort(reverse=True)
    # get coordintates
    ax = fig.gca()
    msg_game_clock = 'game clock: ' + str(instance_array[0][0])
    msg_shot_clock = 'shot clock: ' + str(instance_array[0][1])
    msg_ball_height = 'ball height: ' + str(grouped_fixedtime.get_group(instance_array[0]).moment.iloc[0])

    game_clock_annotations = ax.text(-18, 25, msg_game_clock)
    shot_clock_annotations = ax.text(-18, 20, msg_shot_clock)
    ball_height_annotations = ax.text(-18, 15, msg_ball_height)

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

    x_home, y_home, jersey_home = team_coord(idx_num=0, team_id=hometeam_id, dataframe=df_fixedtime)
    x_away, y_away, jersey_away = team_coord(idx_num=0, team_id=visitorteam_id, dataframe=df_fixedtime)

    # initial ball coordinates
    x_ball, y_ball, ball_id = team_coord(idx_num=0, team_id=-1, dataframe=df_fixedtime)

    # plot the initial point
    scat_home = plot_points(ax, x_home, y_home, color='blue')
    scat_away = plot_points(ax, x_away, y_away, color='red')
    scat_ball = plot_points(ax, x_ball, y_ball, color='black')

    # label the coordinates
    home_annotations = annotate_points(ax, x_home, y_home, jersey_home)
    away_annotations = annotate_points(ax, x_away, y_away, jersey_away)

    def update(frame_number):
        x_home, y_home, jeresy_home = team_coord(
            frame_number, hometeam_id, df_fixedtime)
        x_away, y_away, jeresy_away = team_coord(
            frame_number, visitorteam_id, df_fixedtime)
        x_ball, y_ball, ball_id = team_coord(
            frame_number, -1, df_fixedtime)

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
            'ball height: ' + str(grouped_fixedtime.get_group(instance_array[frame_number]).moment.iloc[0]))

    # number of frames
    no_frame = len(instance_array)

    anim = animation.FuncAnimation(fig, init_func=init, func=update, frames=no_frame, blit=False, interval=10, repeat=False)

    # anim.save('play.mpeg', fps=10, extra_args=['-vcodec', 'libx264'])

    return anim




    period = 1
    time_start = 665
    time_end = 663
    #
    # # There is a glitch with these times, quarter 1
    # # time_start = 394
    # # time_end = 393

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    anim = play_animation(period, time_start, time_end, fig, game_info_dict=game_info_dict, dataframe=df_raw_position_data)
    plt.show()
    plt.ioff()


cols = ['period', u'game_clock', 'game_time_remain', u'shot_clock', 'x_loc',
        u'y_loc', u'moment', u'dist_to_ball', u'closest_to_ball',
        u'player_name']

##############################################
##############################################
##############################################
##############################################
# OLD ONE #

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from triple_triple.full_court import draw_court
from triple_triple.startup_data import (
    get_player_ids,
    get_game_id_dict,
    get_df_positions,
    get_df_raw_position_data,
)

player_ids = get_player_ids()
game_id_dict = get_game_id_dict()
df_positions = get_df_positions()
df_raw_position_data = get_df_raw_position_data()



##############################################
# Animation of one player using df_raw_position_data
##############################################

def animate_player_raw_position(start_index, stop_index, playerid, plot_colour,
                                dataframe=df_raw_position_data):
    # from df_raw_position_data
    df_raw_player = dataframe[dataframe['player_id'] == int(playerid)]
    # OR from df_positions (but have to change jersey number)
    # df_raw_player = df_positions[player]

    fig = plt.figure(figsize=(15, 9))
    ax = draw_court()
    ax.set_xlim([0, 94])
    ax.set_ylim([0, 50])

    # coordinates to plot
    x_coord = np.array(df_raw_player['x_loc'][start_index:stop_index])
    y_coord = np.array(df_raw_player['y_loc'][start_index:stop_index])

    # initial point to plot
    scat = ax.scatter([x_coord[0]], [y_coord[0]], color=plot_colour, s=400)

    # label coordinates:
    jersey_number = df_raw_player['player_jersey'].iloc[start_index]
    x = x_coord[0]
    y = y_coord[0]
    annotation = ax.annotate(jersey_number, xy=(x - .5, y - .4))

    # initialize function. Plot the background of each frame
    def init():
        scat.set_offsets([])
        return scat, annotation

    # animation function.  This is called sequentially
    def update(frame_number):
        scat.set_offsets(np.array([x_coord[frame_number], y_coord[frame_number]]))
        x = x_coord[frame_number]
        y = y_coord[frame_number]
        annotation.set_position((x - .5, y - .4))
        return scat, annotation

    no_frames = len(x_coord)
    anim = animation.FuncAnimation(fig, update, init_func=init,
                                   frames=no_frames, interval=10)

    # had to use VLC to play movies (not Quicktime)
    # anim.save('player_movement.mp4fps=30,extra_args=['-vco'libx264'])
    plt.show()
    return anim


def playerid_from_name(player_name, player_info_dict=game_id_dict):
    for playerid, player_info in game_id_dict.items():
        if player_info[0] == player_name:
            return playerid

# def playerid_from_name(player, player_ids):
#     for key, value in player_ids.items():
#         if value[1]==player:
#             return key


def fixedtime_df(period, time_start, time_end, dataframe=df_positions):

    return dataframe[
        (dataframe.game_clock.values <= time_start) &
        (dataframe.game_clock.values >= time_end) &
        (dataframe.period.values == period)
    ]


def player_coord(player_name, dataframe=df_positions):
    df_player = dataframe[player_name]
    x_coord = np.array(df_player['x_loc'])
    y_coord = np.array(df_player['y_loc'])
    return x_coord, y_coord


def team_coord(index_number, team_id, dataframe=df_positions,
               player_info_dict=game_id_dict):

    # this needs .sort_index(axis=1)
    # in get_df_positions function (startup_data.py)
    df_pos_x_loc = dataframe.loc[:, (slice(None), 'x_loc')]
    df_pos_y_loc = dataframe.loc[:, (slice(None), 'y_loc')]

    # player info: (name, jersey, team_id)
    # excluding the ball
    player_details = [
        [x[0],
         game_id_dict[playerid_from_name(x[0])][1],
         game_id_dict[playerid_from_name(x[0])][2]]
        for x in list(df_pos_x_loc.columns)[:-1]
    ]

    x_coord = df_pos_x_loc.values[index_number]
    y_coord = df_pos_y_loc.values[index_number]

    # only keep coord for team_id
    # find indices that we want to delete:
    other_team_indicies = [
        k for k, item in enumerate(player_details)
        if item[2] != team_id
    ]

    x_coord = np.delete(x_coord, other_team_indicies, axis=0)
    y_coord = np.delete(y_coord, other_team_indicies, axis=0)
    player_details = np.delete(player_details, other_team_indicies, axis=0)

    return x_coord, y_coord, player_details


def plot_points(ax, x_points, y_points, color):
    return ax.scatter(x_points, y_points, color=color, s=400)


def annotate_points(ax, xx, yy, player):
    return [
        ax.annotate(jersey_number[1], xy=(x - 0.5, y - 0.4))
        for x, y, jersey_number in zip(xx, yy, player)
    ]


def update_annotations(annotations, xx, yy):
    for x, y, anno in zip(xx, yy, annotations):
        anno.set_position((x - 0.5, y - 0.4))

##############################################
# Animation of all players using df_positions
##############################################

# if player is None, plots all players
# if player = [player_id, jersey, team_id, position]
# it only plots that player's movement


def play_animation(period, time_start, time_end, fig, dataframe=df_positions,
                   hometeam_id=None, awayteam_id=None, player=None):

    fixedtime = fixedtime_df(period, time_start, time_end)
    game_clock_array = fixedtime.game_clock.values.flatten()
    shot_clock_array = fixedtime.shot_clock.values.flatten()
    ball_height_array = fixedtime.ball_height.values.flatten()

    # get coordintates
    ax = fig.gca()
    msg_game_clock = 'game clock: ' + str(game_clock_array[0])
    msg_shot_clock = 'shot clock: ' + str(shot_clock_array[0])
    msg_ball_height = 'ball height: ' + str(shot_clock_array[0])

    game_clock_annotations = ax.text(-18, 25, msg_game_clock)
    shot_clock_annotations = ax.text(-18, 20, msg_shot_clock)
    ball_height_annotations = ax.text(-18, 15, msg_ball_height)

    if player is None:
        # initialize the
        # each frame
        def init():
            game_clock_annotations.set_text('initial')
            shot_clock_annotations.set_text('initial')
            ball_height_annotations.set_text('initial')
            scat_home.set_offsets([])
            scat_away.set_offsets([])
            scat_ball.set_offsets([])
            return scat_home, scat_away, scat_ball, game_clock_annotations, \
                shot_clock_annotations, ball_height_annotations

        # initial coordinates:
        # players
        x_home, y_home, player_home = team_coord(0, hometeam_id, fixedtime)
        x_away, y_away, player_away = team_coord(0, awayteam_id, fixedtime)

        # iniial ball coordinates
        x_ball, y_ball, ball_id = team_coord(0, '-1', fixedtime)

        # plot the initial point
        scat_home = plot_points(ax, x_home, y_home, color='blue')
        scat_away = plot_points(ax, x_away, y_away, color='red')
        scat_ball = plot_points(ax, x_ball, y_ball, color='black')

        # label the coordinates
        home_annotations = annotate_points(ax, x_home, y_home, player_home)
        away_annotations = annotate_points(ax, x_away, y_away, player_away)

        # add quarter and time
        # quarter_annotations = ax.annotate('quarter: ' + str(period), (-15, 30))

        def update(frame_number):
            x_home, y_home, player_home = team_coord(frame_number,
                                                     hometeam_id, fixedtime)
            x_away, y_away, player_away = team_coord(frame_number,
                                                     awayteam_id, fixedtime)
            x_ball, y_ball, ball_id = team_coord(frame_number, -1, fixedtime)

            # set_offsets expects N x 2 array
            data_home = np.array([x_home, y_home]).T
            data_away = np.array([x_away, y_away]).T
            scat_home.set_offsets(data_home)
            scat_away.set_offsets(data_away)
            scat_ball.set_offsets((x_ball, y_ball))

            update_annotations(home_annotations, x_home, y_home)
            update_annotations(away_annotations, x_away, y_away)

            # update game_clock and shot_clock:
            game_clock_annotations.set_text('game clock: ' +
                                            str(game_clock_array[frame_number]))
            shot_clock_annotations.set_text('shot clock: ' +
                                            str(shot_clock_array[frame_number]))
            ball_height_annotations.set_text('ball height: ' +
                                             str(ball_height_array[frame_number]))

        # number of frames
        no_frame = len(fixedtime)

        anim = animation.FuncAnimation(fig, init_func=init, func=update,
                                       frames=no_frame, blit=False,
                                       interval=10, repeat=False)

        # anim.save('play.mpeg', fps=10, extra_args=['-vcodec', 'libx264'])

        return anim

    elif player is not None:
        fixedtime = fixedtime_df(period, time_start, time_end)
        game_clock_array = fixedtime.game_clock.values.flatten()
        shot_clock_array = fixedtime.shot_clock.values.flatten()
        ball_height_array = fixedtime.ball_height.values.flatten()

        ax = fig.gca()
        msg_game_clock = 'game clock: ' + str(game_clock_array[0])
        msg_shot_clock = 'shot clock: ' + str(shot_clock_array[0])
        msg_ball_height = 'ball height: ' + str(shot_clock_array[0])
        game_clock_annotations = ax.text(-15, 25, msg_game_clock)
        shot_clock_annotations = ax.text(-15, 20, msg_shot_clock)
        ball_height_annotations = ax.text(-15, 15, msg_ball_height)

        def init():
            game_clock_annotations.set_text('initial')
            shot_clock_annotations.set_text('initial')
            ball_height_annotations.set_text('initial')
            scat_player.set_offsets([])
            scat_ball.set_offsets([])
            return scat_player, scat_ball, game_clock_annotations, \
                shot_clock_annotations, ball_height_annotations

        # Get coordintates
        x_coord, y_coord = player_coord(player, fixedtime)
        x_ball_coord, y_ball_coord = player_coord('ball', fixedtime)

        playerid = playerid_from_name(player)
        team = game_id_dict[playerid][2]

        # plot initial points
        if team == hometeam_id:
            color = 'blue'

        elif team == awayteam_id:
            color = 'red'

        scat_player = plot_points(ax, x_coord[0], y_coord[0], color=color)
        scat_ball = plot_points(ax, x_ball_coord[0], y_ball_coord[0], color='black')

        # label coordinates:
        jersey_number = game_id_dict[playerid][1]
        annotation = ax.annotate(jersey_number, xy=(x_coord[0] - .5, y_coord[0] - .4))

        # add quarter and time
        # quarter_annotations = ax.annotate('quarter: ' + str(period), (-15, 30))

        # animation function.  This is called sequentially
        def update(frame_number):
            x_player = x_coord[frame_number]
            y_player = y_coord[frame_number]
            scat_player.set_offsets((x_player, y_player))
            annotation.set_position((x_player - .5, y_player - .4))

            scat_ball.set_offsets((x_ball_coord[frame_number],
                                   y_ball_coord[frame_number]))
            # update shot_clock, game_clock, ball_height:
            game_clock_annotations.set_text('game clock: ' +
                                            str(game_clock_array[frame_number]))
            shot_clock_annotations.set_text('shot clock: ' +
                                            str(shot_clock_array[frame_number]))
            ball_height_annotations.set_text('ball height: ' +
                                             str(ball_height_array[frame_number]))

        # number of frames
        no_frame = len(x_coord)

        anim = animation.FuncAnimation(fig, func=update, init_func=init,
                                       frames=no_frame, interval=10, blit=False)

        return anim
