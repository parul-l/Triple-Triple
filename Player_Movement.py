import json
import numpy as np
import pandas as pd
from matplotlib import animation
import matplotlib.pyplot as plt
import itertools

from full_court import draw_court
import player_position_data as ppd


        
# determine some shot attempts?
ball_up = df[(df.player_name == 'ball') & 
            (df.game_clock >= 697) & (df.game_clock <698) ]    
plt.scatter(ball_up.x_loc.head(len(ball_up)), ball_up.y_loc.head(len(ball_up)),
            c = ball_up.game_clock.head(len(ball_up)), cmap = plt.cm.Blues, 
            s=500, zorder = 1 )     
bosh = df[(df.player_name == 'Chris Bosh') & 
            (df.game_clock >= 697) & (df.game_clock <698) ]

# display the rows to determine the times I want:            
with pd.option_context('display.max_rows', 200):
    print bosh
                
plt.scatter(ball_up.x_loc.head(len(bosh)), ball_up.y_loc.head(len(bosh)), 
            c = ball_up.game_clock.head(len(bosh)), cmap = plt.cm.Reds, 
            s=500, zorder = 1 )                

wade = df[df.player_name =='Dwyane Wade']
wade_time = df[(df.player_name =='Dwyane Wade') & (df.game_clock == 720)]


#######################
# Plot of Wade's movement
#######################

fig = plt.figure(figsize=(15,9))
full_court()
plt.xlim([0, 94])
plt.ylim([0, 50])
# plt.axis('off')
plt.show()   

#number of points to plot
n = len(wade)
plt.scatter(wade.x_loc.head(n), wade.y_loc.head(n), cmap = plt.cm.Blues, s=100, zorder=1)

#plt.scatter(wade.x_loc.head(n), wade.y_loc.head(n), c = wade.game_clock.head(n), cmap = plt.cm.Blues, s=1000, zorder=1)

cbar = plt.colorbar(orientation = "horizontal")
cbar.ax.invert_xaxis()

#######################
# Animation 
#######################

fig = plt.figure(figsize=(15,9))
ax = full_court()
 
# coordinates to plot
n = 500
x_coord = np.array(wade['x_loc'][:n])
y_coord = np.array(wade['y_loc'][:n]) 

#initial point to plot
scat = ax.scatter([x_coord[0]], [y_coord[0]], color = 'blue', s=400)

# Label coordinates:
jersey_number = 3
x = x_coord[0]
y = y_coord[0]
text = jersey_number              
annotation = ax.annotate(text, xy = (x-.5, y-.4))


# initialize function. Plot the background of each frame
def init():
    scat.set_offsets([])
    return scat, annotation
    

# animation function.  This is called sequentially
def update(frame_number):
    scat.set_offsets(np.array([x_coord[frame_number], y_coord[frame_number]]))
    x = x_coord[frame_number]
    y = y_coord[frame_number]            
    annotation.set_position((x-.5, y-.4))
    return scat, annotation
    
anim = animation.FuncAnimation(fig, update, init_func=init, 
                            frames =500, interval=10)

# Not able to play saved movies. I'm not sure why.
# anim.save('player_movement.mp4', fps=30, extra_args=['-vcodec', 'libx264'])                            
                            
plt.show()


# Create the animation using df_positions
fig = plt.figure(figsize=(15,9))
ax = full_court()

# Wades's first n coordinates
n = 200
x_coord, y_coord = zip(*df_positions[wade][:n])

#initial point to plot
scat = ax.scatter(x_coord[0], y_coord[0], color = 'blue', s=400)

# Label coordinates:
jersey_number = 3
x = x_coord[0]
y = y_coord[0]           
annotation = ax.annotate(jersey_number, xy = (x-.5, y-.4))

# initialize function. Plot the background of each frame
def init():
    scat.set_offsets([])
    return scat, annotation
    
# animation function.  This is called sequentially
def update(frame_number):
    scat.set_offsets((x_coord[frame_number], y_coord[frame_number]))
    x = x_coord[frame_number]
    y = y_coord[frame_number]            
    annotation.set_position((x-.5, y-.4))
    return scat, annotation
    
anim = animation.FuncAnimation(fig, update, init_func=init, frames =n, interval=10)    
    
plt.show()  

###################
###################

def df_fixedtime(df_positions, period, time_start, time_end):
    return df_positions[(df_positions.game_clock <= time_start) &
                        (df_positions.game_clock >= time_end) &
                        (df_positions.period == period)
                        ]  

def player_coord(player_info, dataframe):
    df_temp = dataframe[player_info]
    # remove rows of zeros
    df_temp = df_temp[df_temp!=0]
    
    return zip(*df_temp) 

def all_players_coord(array, team_id):
    x_coord = []
    y_coord = []
    player = []
        
    for i in range(2, len(headers_pos)):
        if headers_pos[i][3] == team_id and array[i][0] >=0:    
            x_coord.append(array[i][0])
            y_coord.append(array[i][1])
            player.append(headers_pos[i])
    
    return x_coord, y_coord, player      

def plot_points(ax,x_points, y_points, color):
    return ax.scatter(x_points, y_points, color=color, s=400)
    
     
def annotate_points(ax, xx, yy, player):
    return [ax.annotate(jersey_number[2], xy=(x-.5, y-.4))
 for x, y, jersey_number in zip(xx, yy, player)]


def update_annotations(annotations, xx, yy):
    for x, y, anno in zip(xx, yy, annotations):
        anno.set_position((x - 0.5, y - 0.4))

# Animation function:
# if player is None, plots all players 
# if player = [player_id, jersey, team_id, position]
# it only plots that player's movement
        
def play_animation(df_positions, period, time_start, time_end, fig,
                    hometeam_id = None, awayteam_id = None, player=None):
    
    fixedtime = df_fixedtime(df_positions, period, time_start, time_end)
    # Get coordintates
    ax = fig.gca()    
    
    if player is None:
        # initialize the 
        # each frame
        def init():
            scat_home.set_offsets([])
            scat_away.set_offsets([])
            scat_ball.set_offsets([])
            return scat_home, scat_away, scat_ball,
        
        # initial coordinates:
        # players
        x_home, y_home, player_home = all_players_coord(fixedtime.values[0], hometeam_id)
        x_away, y_away, player_away = all_players_coord(fixedtime.values[0], awayteam_id)
        
        # iniial ball coordinates
        x_ball, y_ball, ball_id = all_players_coord(fixedtime.values[0], -1)

        # plot the initial point    
        scat_home = plot_points(ax, x_home, y_home, color = 'blue')
        scat_away = plot_points(ax, x_away, y_away, color = 'red')
        scat_ball = plot_points(ax, x_ball, y_ball, color = 'black')
        
        # Label the coordinates
        home_annotations = annotate_points(ax, x_home, y_home, player_home)
        away_annotations = annotate_points(ax, x_away, y_away, player_away)
        
        def update(frame_number):
            x_home, y_home, player_home =   all_players_coord(fixedtime.values[frame_number], hometeam_id)
            x_away, y_away, player_away =   all_players_coord(fixedtime.values[frame_number], awayteam_id)
            x_ball, y_ball, ball_id = all_players_coord(fixedtime.values[frame_number], -1)
            
            data_home = np.array([x_home, y_home]).T
            data_away = np.array([x_away, y_away]).T
            scat_home.set_offsets(data_home)
            scat_away.set_offsets(data_away)
            scat_ball.set_offsets((x_ball, y_ball)) 

            update_annotations(home_annotations, x_home, y_home)
            update_annotations(away_annotations, x_away, y_away)

        # Number of frames
        no_frame = len(fixedtime)

        anim = animation.FuncAnimation(fig, init_func=init, func=update,frames=no_frame, blit = False, interval=10, repeat = False)
        
        anim.save('play.mpeg', fps=10, extra_args=['-vcodec', 'libx264'])
     

        return anim
    # THIS PART NOT RECOGNIZING COLOR!!! WTHHH             
    else:
        x_coord, y_coord = player_coord(player, fixedtime)
        # Plot initial points
        
        if player[3] == hometeam_id:
            color = 'blue'
            
        elif player[3] == awayteam_id:
            color = 'red'

        scat = plot_points(ax, x_coord[0], y_coord[0], color=color)
        
        # Label coordinates:
        jersey_number = player[2]
        annotation = ax.annotate(jersey_number, xy=(x_coord[0]-.5,y_coord[0]-.4)) 
        
        # animation function.  This is called sequentially
        def update(frame_number):
            x = x_coord[frame_number]
            y = y_coord[frame_number] 
            scat.set_offsets((x, y))      
            annotation.set_position((x-.5, y-.4))
        
        # Number of frames
        no_frame = len(x_coord)
        
        anim = animation.FuncAnimation(fig, func=update, frames=no_frame, interval=10, blit = False)    
        plt.show()
        
        return anim
        
        
######################
wade = (2548, u'Dwyane Wade', u'3', 1610612748, u'G')

hometeam_id = 1610612744
awayteam_id = 1610612748
period = 2
time_start = 10
time_end = 5

# There is a glitch with these times, quarter 1 
# time_start = 394
# time_end = 393

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
anim = play_animation(df_positions, fig= fig, period = period, time_start = time_start, time_end =time_end, hometeam_id = hometeam_id, awayteam_id = awayteam_id)
anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
plt.show()
plt.ioff()  
             

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)    
play_animation(df_positions, fig= fig, period = 1, time_start = 402, 
                time_end =350, player = wade)
plt.ioff()   


###########################
# Still image for Data Incubator
#########################
fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax) 
fixedtime = df_fixedtime(df_positions, period, time_start, time_end)
# Get coordintates
ax = fig.gca()    



# initial coordinates:
# players
x_home, y_home, player_home = all_players_coord(fixedtime.values[0],hometeam_id)
x_away, y_away, player_away = all_players_coord(fixedtime.values[0],awayteam_id)

# iniial ball coordinates
x_ball, y_ball, ball_id = all_players_coord(fixedtime.values[0], -1)

# plot the initial point    
scat_home = ax.scatter(x_home, y_home, color='blue', s=400, 
            label='Golden State Warriors') 
scat_away = ax.scatter(x_away, y_away, color = 'red', s=400,
            label='Miami Heat')
scat_ball = ax.scatter(x_ball, y_ball, color = 'black', s=400, label = 'ball')

# Label the coordinates
home_annotations = annotate_points(ax, x_home, y_home, player_home)
away_annotations = annotate_points(ax, x_away, y_away, player_away)

plt.title('Snap shot of MIA @ GSW \n January 11, 2016' )
plt.legend(loc='lower left')
fig.savefig('allplayers.png') 
plt.show()                             
