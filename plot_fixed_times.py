import matplotlib.pyplot as plt
from matplotlib import animation

# Don't think I'm importing these correctly
from full_court import draw_court
from play_by_play_nbastats import play_by_play
from player_position_data import df_raw_position_data

# display the rows to determine the times I want:            
with pd.option_context('display.max_rows', 200):
    print df_raw_position_data
            
# Determie all players on court at given period and time within one frame
# of time provided (like when player x scored using player_shot_info)
def all_players_at_fixed_time(period, time, dataframe=df_raw_position_data): 
    return dataframe[ (dataframe.period == period) &
            (dataframe.game_clock - time< 0.04) &
            (dataframe.game_clock - time>=0)]
            
# Plot ONE player at a fixed time range
def plot_player_at_fixed_times(player, period, time_start, 
                                time_end,color, dataframe=df_raw_position_data):
    player_fixed_time = dataframe[(dataframe.player_name == player) & 
                        (dataframe.period == period) &
                        (dataframe.game_clock <= time_start) &
                        (dataframe.game_clock >= time_end)]
    
    n = len(player_fixed_time)
    plt.scatter(player_fixed_time.x_loc.head(n), 
                player_fixed_time.y_loc.head(n), 
                c = player_fixed_time.game_clock.head(n), 
                cmap = color, s=400, zorder=1)

    # Label coordinates:
    x = player_fixed_time.iloc[n-1]['x_loc']
    y = player_fixed_time.iloc[n-1]['y_loc']
    text = player_fixed_time.iloc[0]['player_jersey']               
    label = ax.annotate(text, xy = (x-.6, y-.4))
    
    # gradient legend: ok for this plot but not for
    # plot_all_players_fixed_time (which uses this plot)
    
    # cbar = plt.colorbar(orientation = "horizontal")
    # cbar.ax.invert_xaxis()

def plot_all_players_fixed_time(period, time, away_team, home_team, dataframe=df_raw_position_data):
    ap_fixedtime = all_players_at_fixed_time(period, time) 
    for i in range(11):
        player  = ap_fixedtime['player_name'].iloc[i]
        time    = ap_fixedtime['game_clock'].iloc[i]
        
        if ap_fixedtime['player_name'].iloc[i] =='ball':
            color = plt.cm.gray
        
        elif ap_fixedtime['team_id'].iloc[i] == away_team:
            color = plt.cm.winter
            
        elif ap_fixedtime['team_id'].iloc[i] == home_team:
            color = plt.cm.autumn    
            
        plot_player_at_fixed_times(player, period, time, time, color)    

           
player = 'Dwyane Wade'
home_team = 1610612748
away_team = 1610612744
period = 1
time_start = 402
time_end = 400

plt.figure(figsize=(15,9))
ax = draw_court()
ax.set_xlim([0,94])
ax.set_ylim([0,50])
plt.show() 

plot_player_at_fixed_times(player, period, time_start, time_end, dataframe=df_raw_position_data, color = 'winter')

######################
plt.figure(figsize=(15,9))
ax = draw_court()
ax.set_xlim([0,94])
ax.set_ylim([0,50])
plt.show() 

plot_all_players_fixed_time(period, time_start, away_team, home_team, dataframe=df_raw_position_data)

plt.title('Snap shot of MIA @ GSW \n January 11, 2016' )
plt.legend(loc='lower left')
fig.savefig('allplayers.png') 

#########################
#########################
# Still image for Data Incubator
#########################
#########################

# functions used here are defined in play_animation.py 

hometeam_id = '1610612744'
awayteam_id = '1610612748'
period = 2
time_start = 100
time_end = 5

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax) 
fixedtime = df_fixedtime(period, time_start, time_end)
# Get coordintates
ax = fig.gca()    

# initial coordinates:
# players
x_home, y_home, player_home = all_players_coord(0, hometeam_id, fixedtime)
x_away, y_away, player_away = all_players_coord(0, awayteam_id, fixedtime)

# iniial ball coordinates
x_ball, y_ball, ball_id = all_players_coord(0, -1, fixedtime)

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
