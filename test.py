import itertools

from matplotlib import animation
import matplotlib.collections as mc
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


from full_court import draw_court

##################
##################
##################

length  = len(play_by_play)

for i in range(length):
    if type(play_by_play[i][7]) == list:
        print i, play_by_play[i]   
        
wade_shot1 = df[(df.game_clock >= 401) & (df.game_clock <401.05) ]

####################
len_events = len(data['events'])
player_moments2 = []
# create a list that contains all the header info for each moment
for m in range(1, len_events):
    len_moment = len(data['events'][m]['moments'])    
    for i in range(len_moment):
        #len_moment = len(data['events'][m]['moments'][i][5])
        for item in data['events'][m]['moments'][i][5]:
            item.append(
            data['events'][m]['moments'][i][2]
            )
            item.append(
            data['events'][m]['moments'][i][3]
            )
            player_moments2.append(item)  
            
#############
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(15, 9))
ax = draw_court()

n = 500  
x = np.array(wade['x_loc'][:n])
y = np.array(wade['y_loc'][:n])

# initialize

line, = ax.plot(x[0], y[0], 'o', color="blue")

def update():
    for i in range(1,500):
        x[0], y[0] = x[i], y[i]
        yield x, y

def draw(n):
    line.set_xdata(x[0])
    line.set_ydata(y[0])
    return line,
    
anim = animation.FuncAnimation(fig, draw, update, 
                            interval=500, blit=False)
plt.show()            
                    
################
################
################
execfile('/Users/pl/Dropbox/Triple-Triple/draw_court.py')
fig = plt.figure(figsize=(15,9))
ax = draw_court()
 
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
plt.show()

##############################
#############################

# Get players coordinates at certain time

def player_coord(player_info, period, time):
    df_temp = df_positions[(df_positions.game_clock==time) & (df_positions.period==period)]
    df_temp = df_temp[player_info]
    # remove rows of zeros
    df_temp = df_temp[df_temp!=0]
    
    return zip(*df_temp) 

def plot_points(x_points, y_points, color):
    ax.scatter(x_points, y_points, color = color, s = 400)
    plt.show()



fig = plt.figure(figsize=(15,9))
ax = draw_court()

period = 4
time = 3.14
# initialize the points to plot    
x_points = []
y_points = []   
for item in players_that_played:
    try:
        x, y = player_coord(item, period, time)
        # For a specific time, we expect only one point
        # But for example, t = 720 contains many points
        # I assume, moving around at the start of the quarter
        x_points.append(x[0])
        y_points.append(y[0])
        
        # Plot initial points
        if item[2] == 1610612744:
            color = 'blue'
            
        elif item[2] == 1610612748:
            color = 'red'
            
        plot_points(x, y, color)   
        # Label coordinates:
        jersey_number = item[1]
        text = jersey_number              
        annotation = ax.annotate(text, xy = (x[0]-.5, y[0]-.4)) 
    except:
        pass  
########################        
########################
########################
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
        
    for i in range(2, len(headers_loc)):
        if headers_loc[i][2] == team_id and array[i][0] >=0:    
            x_coord.append(array[i][0])
            y_coord.append(array[i][1])
            player.append(headers_loc[i])
    
    return x_coord, y_coord, player      

def plot_points(ax,x_points, y_points, color):
    return ax.scatter(x_points, y_points, color=color, s=400)
    
     
def annotate_points(ax, xx, yy, player):
    return [ax.annotate(jersey_number[1], xy=(x-.5, y-.4))
 for x, y, jersey_number in zip(xx, yy, player)]


def update_annotations(annotations, xx, yy):
    for x, y, anno in zip(xx, yy, annotations):
        anno.set_position((x - 0.5, y - 0.4))


# Draw the court
fig = plt.figure(figsize=(15,9))
ax = draw_court()

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = full_court(ax)

player = wade
hometeam_id = 1610612744
awayteam_id = 1610612748
period = 1
time_start = 402
time_end = 401


def play_animation(df_positions, player, period, time_start, time_end, fig):
    fixedtime = df_fixedtime(df_positions, period, time_start, time_end)
    # Get coordintates
    ax = fig.gca()
    
    x_coord, y_coord = player_coord(player, fixedtime)
    # Plot initial points
    if player[2] == 1610612744:
        color = 'blue'
        
    elif player[2] == 1610612748:
        color = 'red'

    # plot the initial point    
    scat = plot_points(ax, x_coord[0], y_coord[0], color)
       
    # Label coordinates:
    jersey_number = player[1]
    annotation = ax.annotate(jersey_number, xy=(x_coord[0]-.5, y_coord[0]-.4)) 
        
    # animation function.  This is called sequentially
    def update(frame_number):
        x = x_coord[frame_number]
        y = y_coord[frame_number] 
        scat.set_offsets((x, y))      
        annotation.set_position((x-.5, y-.4))

    # Number of frames
    no_frame = len(x_coord)

    anim = animation.FuncAnimation(fig, func=update, frames=no_frame, 
                                   interval=10)    
    plt.show()


#####################
#####################
def play_animation2(df_positions, period, time_start, time_end, fig,
                    hometeam_id = None, awayteam_id = None, player=None):
    
    fixedtime = df_fixedtime(df_positions, period, time_start, time_end)
    # Get coordintates
    ax = fig.gca()
    
    
    if player == None:
        
        # initial coordinates:
        x_home, y_home, player_home = all_players_coord(fixedtime.values[0], hometeam_id)
        x_away, y_away, player_away = all_players_coord(fixedtime.values[0], awayteam_id)

        # plot the initial point    
        scat_home = plot_points(ax, x_home, y_home, color = 'blue')
        scat_away = plot_points(ax, x_away, y_away, color = 'red')
        
        # # Label the coordinates
        # for i in range(len(x_home)):
        #     annotate_points(ax, x_home[i], y_home[i], player_home[i])
        # for i in range(len(x_away)):
        #     annotate_points(ax, x_away[i], y_away[i], player_away[i])    
        # 
        # Probably need to do this instead (for animation purposes)
        
        ax_home0 = annotate_points(ax, x_home[0], y_home[0], player_home[0])
        ax_home1 = annotate_points(ax, x_home[1], y_home[1], player_home[1])
        ax_home2 = annotate_points(ax, x_home[2], y_home[2], player_home[2])
        ax_home3 = annotate_points(ax, x_home[3], y_home[3], player_home[3])
        ax_home4 = annotate_points(ax, x_home[4], y_home[4], player_home[4])
        
        ax_away0 = annotate_points(ax, x_away[0], y_away[0], player_away[0])
        ax_away1 = annotate_points(ax, x_away[1], y_away[1], player_away[1])
        ax_away2 = annotate_points(ax, x_away[2], y_away[2], player_away[2])
        ax_away3 = annotate_points(ax, x_away[3], y_away[3], player_away[3])
        ax_away4 = annotate_points(ax, x_away[4], y_away[4], player_away[4])
        
        # initialize function. Plot the background of each frame
        def init():
            scat.set_offsets([])
            return scat_home, scat_away, ax_home0, ax_home1, ax_home2, ax_home3, ax_home4, ax_away0, ax_away1, ax_away2, ax_away3, ax_away4 
        
        def update(frame_number):
            x_home, y_home, player_home =   all_players_coord(fixedtime.values[frame_number], hometeam_id)
            x_away, y_away, player_away =   all_players_coord(fixedtime.values[frame_number], awayteam_id)
            
            data_home = np.array([x_home, y_home]).T
            data_away = np.array([x_away, y_away]).T
            scat_home.set_offsets(data_home)
            scat_away.set_offsets(data_away) 
            
            ax_home0.set_position((x_home[0]-0.5, y_home[0]-0.4))
            ax_home1.set_position((x_home[1]-0.5, y_home[1]-0.4))
            ax_home2.set_position((x_home[2]-0.5, y_home[2]-0.4))
            ax_home3.set_position((x_home[3]-0.5, y_home[3]-0.4))
            ax_home4.set_position((x_home[4]-0.5, y_home[4]-0.4))
            
            ax_away0.set_position((x_away[0]-0.5, y_away[0]-0.4))
            ax_away1.set_position((x_away[1]-0.5, y_away[1]-0.4))
            ax_away2.set_position((x_away[2]-0.5, y_away[2]-0.4))
            ax_away3.set_position((x_away[3]-0.5, y_away[3]-0.4))
            ax_away4.set_position((x_away[4]-0.5, y_away[4]-0.4))
                
        
        # Number of frames
        no_frame = len(fixedtime)

        anim = animation.FuncAnimation(fig, func=update, frames=no_frame, 
                               interval=10)    
        plt.show()
        
                   
    else:
        x_coord, y_coord = player_coord(player, fixedtime)
        # Plot initial points
        if player[2] == 1610612744:
            color = 'blue'
            
        elif player[2] == 1610612748:
            color = 'red'

            # plot the initial point    
            scat = plot_points(ax, x_coord[0], y_coord[0], color)
            
            # Label coordinates:
            jersey_number = player[1]
            annotation = ax.annotate(jersey_number, xy=(x_coord[0]-.5, y_coord[0]-.4)) 
            
            # animation function.  This is called sequentially
            def update(frame_number):
                x = x_coord[frame_number]
                y = y_coord[frame_number] 
                scat.set_offsets((x, y))      
                annotation.set_position((x-.5, y-.4))

        # Number of frames
        no_frame = len(x_coord)

        anim = animation.FuncAnimation(fig, func=update, frames=no_frame, 
                                   interval=10)    
        plt.show()


    

player = wade
hometeam_id = 1610612744
awayteam_id = 1610612748
period = 1
time_start = 402
time_end = 395

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
play_animation(df_positions, 1, 402, 350, fig, hometeam_id = hometeam_id, 
awayteam_id = awayteam_id)
plt.show()

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
play_animation2(df_positions, 1, 402, 350, fig, player = wade)
plt.show()


#################
#################
#################
# This saves animations!!!
#################
#################

fixedtime = df_fixedtime(df_positions, period, time_start,time_end)
# Get coordintates
ax = fig.gca()

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)

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
x_ball, y_ball, ball_id =all_players_coord(fixedtime.values[0], -1)

# plot the initial point    
scat_home = plot_points(ax, x_home, y_home, color ='blue')
scat_away = plot_points(ax, x_away, y_away, color = 'red')
scat_ball = plot_points(ax, x_ball, y_ball, color ='black')

# Label the coordinates
home_annotations = annotate_points(ax, x_home, y_home,player_home)
away_annotations = annotate_points(ax, x_away, y_away,player_away)

def update(frame_number):
    x_home, y_home, player_home = all_players_coord(fixedtime.values[frame_number],hometeam_id)
    x_away, y_away, player_away = all_players_coord(fixedtime.values[frame_number],awayteam_id)
    x_ball, y_ball, ball_id =all_players_coord(fixedtime.values[frame_number],-1)
    
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

plt.show() 

time_start = 402
time_end = 398
