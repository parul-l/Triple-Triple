import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation

from triple_triple.full_court import draw_court
from triple_triple.startup_data import (
    get_player_ids,
    get_game_id_dict,
    get_df_positions,
    get_df_raw_position_data,
    get_df_play_by_play,
    get_df_player_bio_info
)


player_ids = get_player_ids()
game_id_dict = get_game_id_dict()
df_positions = get_df_positions()
df_raw_position_data = get_df_raw_position_data()
df_play_by_play = get_df_play_by_play()
df_player_bio_info = get_df_player_bio_info()

##############################################
# Animation of one player using df_raw_position_data
##############################################

def animate_player_raw_position(start_index, stop_index, playerid, plot_colour,
        dataframe=df_raw_position_data):
    # from df_raw_position_data
    df_raw_player = dataframe[dataframe['player_id']==int(playerid)]
    # OR from df_positions (but have to change jersey number)
    # df_raw_player = df_positions[player]

    fig = plt.figure(figsize=(15,9))
    ax = draw_court()
    ax.set_xlim([0,94])
    ax.set_ylim([0,50])

    # coordinates to plot
    x_coord = np.array(df_raw_player['x_loc'][start_index:stop_index])
    y_coord = np.array(df_raw_player['y_loc'][start_index:stop_index])

    # initial point to plot
    scat = ax.scatter([x_coord[0]], [y_coord[0]],
    color = plot_colour, s=400)

    # label coordinates:
    jersey_number = df_raw_player['player_jersey'].iloc[start_index]
    x = x_coord[0]
    y = y_coord[0]
    annotation = ax.annotate(jersey_number, xy = (x - .5, y - .4))

    # initialize function. Plot the background of each frame
    def init():
        scat.set_offsets([])
        return scat, annotation

    # animation function.  This is called sequentially
    def update(frame_number):
        scat.set_offsets(np.array([x_coord[frame_number],y_coord[frame_number]]))
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

###################
###################
def playerid_from_name(player, player_info_dict=game_id_dict):
    for key, value in game_id_dict.items():
        if value[0] == player:
            return key

# def playerid_from_name(player, player_ids):
#     for key, value in player_ids.items():
#         if value[1]==player:
#             return key


def fixedtime_df(period, time_start, time_end, dataframe=df_positions):

    return dataframe[(dataframe.game_clock.game_clock <= time_start) &
                     (dataframe.game_clock.game_clock >= time_end) &
                     (dataframe.period.period == period)]

def player_coord(player, dataframe = df_positions):
    df_player = dataframe[player]
    x_coord = np.array(df_player['x_loc'])
    y_coord = np.array(df_player['y_loc'])
    return x_coord, y_coord

def team_coord(index_number, team_id, dataframe=df_positions,
        player_info_dict=game_id_dict):

    df_pos_x_loc = dataframe.loc[:, (slice(None), 'x_loc')]
    df_pos_y_loc = dataframe.loc[:, (slice(None), 'y_loc')]

    # player info: (name, jersey, team_id)
    # excluding the ball

    player_details = [
        [
            x[0],
            game_id_dict[playerid_from_name(x[0])][1],
            game_id_dict[playerid_from_name(x[0])][2]
        ] for x in list(df_pos_x_loc.columns)[:-1]
    ]

    x_coord = df_pos_x_loc.values[index_number]
    y_coord = df_pos_y_loc.values[index_number]

    # Only keep coord for team_id
    # find indices that we want to delete:
    other_team_indicies = [
        k for k, item in enumerate(player_details)
        if item[2] != team_id
    ]

    x_coord = np.delete(x_coord, other_team_indicies, axis=0)
    y_coord = np.delete(y_coord, other_team_indicies, axis=0)
    player_details = np.delete(player_details, other_team_indicies, axis=0)

    return x_coord, y_coord, player_details

def plot_points(ax,x_points, y_points, color):
    return ax.scatter(x_points, y_points, color=color, s=400)

def annotate_points(ax, xx, yy, player):
    return [
        ax.annotate(jersey_number[1], xy=(x - .5, y - .4))
        for x, y, jersey_number in zip(xx, yy, player)
    ]

def update_annotations(annotations, xx, yy):
    for x, y, anno in zip(xx, yy, annotations):
        anno.set_position((x - 0.5, y - 0.4))

# Animation function:
# if player is None, plots all players
# if player = [player_id, jersey, team_id, position]
# it only plots that player's movement

def play_animation(period, time_start, time_end, fig, dataframe=df_positions,
        hometeam_id=None, awayteam_id=None, player=None):

    fixedtime = fixedtime_df(period, time_start, time_end)
    game_clock_array = fixedtime.game_clock.game_clock.values
    
    # Get coordintates
    ax = fig.gca()
    msg = 'game clock: ' + str(game_clock_array[0])
    game_clock_annotations = ax.text(-15, 25, msg)

    if player is None:
        # initialize the
        # each frame
        def init():
            game_clock_annotations.set_text('initial')
            scat_home.set_offsets([])
            scat_away.set_offsets([])
            scat_ball.set_offsets([])
            return scat_home, scat_away, scat_ball, game_clock_annotations

        # initial coordinates:
        # players
        x_home, y_home, player_home = team_coord(0, hometeam_id, fixedtime)
        x_away, y_away, player_away = team_coord(0, awayteam_id, fixedtime)

        # iniial ball coordinates
        x_ball, y_ball, ball_id = team_coord(0, '-1', fixedtime)

        # plot the initial point
        scat_home = plot_points(ax, x_home, y_home, color = 'blue')
        scat_away = plot_points(ax, x_away, y_away, color = 'red')
        scat_ball = plot_points(ax, x_ball, y_ball, color = 'black')

        # Label the coordinates
        home_annotations = annotate_points(ax, x_home, y_home, player_home)
        away_annotations = annotate_points(ax, x_away, y_away, player_away)

        # Add quarter and time
        quarter_annotations = ax.annotate('quarter: ' + str(period), (-15, 30))

        def update(frame_number):
            x_home, y_home, player_home = team_coord(frame_number, hometeam_id, fixedtime)
            x_away, y_away, player_away = team_coord(frame_number, awayteam_id, fixedtime)
            x_ball, y_ball, ball_id = team_coord(frame_number, -1, fixedtime)

            # set_offsets expects N x 2 array
            data_home = np.array([x_home, y_home]).T
            data_away = np.array([x_away, y_away]).T
            scat_home.set_offsets(data_home)
            scat_away.set_offsets(data_away)
            scat_ball.set_offsets((x_ball, y_ball))

            update_annotations(home_annotations, x_home, y_home)
            update_annotations(away_annotations, x_away, y_away)

            # update game_clock:
            game_clock_annotations.set_text('game clock: ' + str(game_clock_array[frame_number]))

        # Number of frames
        no_frame = len(fixedtime)

        anim = animation.FuncAnimation(fig, init_func=init, func=update,
            frames=no_frame, blit=False, interval=10, repeat=False)

        #anim.save('play.mpeg', fps=10, extra_args=['-vcodec', 'libx264'])

        return anim

    elif player is not None:
        fixedtime = fixedtime_df(period, time_start, time_end)
        game_clock_array = fixedtime.game_clock.game_clock.values

        ax = fig.gca()
        msg = 'game clock: ' + str(game_clock_array[0])
        game_clock_annotations = ax.text(-15, 25, msg)

        def init():
            game_clock_annotations.set_text('initial')
            scat_player.set_offsets([])
            scat_ball.set_offsets([])
            return scat_player, scat_ball, game_clock_annotations

        # Get coordintates
        x_coord, y_coord = player_coord(player, fixedtime)
        x_ball_coord, y_ball_coord = player_coord('ball', fixedtime)

        playerid = playerid_from_name(player)
        team = game_id_dict[playerid][2]

        # Plot initial points

        if team == hometeam_id:
            color = 'blue'

        elif team == awayteam_id:
            color = 'red'

        scat_player = plot_points(ax, x_coord[0], y_coord[0], color=color)
        scat_ball = plot_points(ax, x_ball_coord[0], y_ball_coord[0], color='black')

        # Label coordinates:
        jersey_number = game_id_dict[playerid][1]
        annotation = ax.annotate(jersey_number,xy=(x_coord[0] - .5, y_coord[0] - .4))
        
        # Add quarter and time
        quarter_annotations = ax.annotate('quarter: ' + str(period), (-15, 30))

        # animation function.  This is called sequentially
        def update(frame_number):
            x_player = x_coord[frame_number]
            y_player = y_coord[frame_number]
            scat_player.set_offsets((x_player, y_player))
            annotation.set_position((x_player - .5, y_player - .4))

            scat_ball.set_offsets((x_ball_coord[frame_number],
                        y_ball_coord[frame_number]))
            # update game_clock:
            game_clock_annotations.set_text('game clock: ' + str(game_clock_array[frame_number]))

        # Number of frames
        no_frame = len(x_coord)

        anim = animation.FuncAnimation(fig,func=update, init_func=init,
            frames=no_frame, interval=10, blit=False)

        return anim

######################
if __name__ == '__main__':

    hometeam_id = '1610612744'
    awayteam_id = '1610612748'
    period = 1
    time_start = 687
    time_end = 685

    # There is a glitch with these times, quarter 1
    # time_start = 394
    # time_end = 393

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    anim = play_animation(fig=fig, period=period, time_start=time_start,
        time_end=time_end, hometeam_id=hometeam_id, awayteam_id=awayteam_id)
    #anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
    plt.show()
    plt.ioff()
    
    ####################
    
    # game clock needs fixing
    # it doesn't remove the previous frame
    player = 'Chris Bosh'
    playerid = playerid_from_name(player)
    plot_colour = 'blue'
    
    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    anim = play_animation(fig=fig, period=period, time_start=time_start,
        time_end=time_end, hometeam_id=hometeam_id, awayteam_id=awayteam_id,
        player=player)
    
    #anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
    plt.show()
    plt.ioff()
