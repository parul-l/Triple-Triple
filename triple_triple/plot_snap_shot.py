import matplotlib.pyplot as plt

from triple_triple.play_animation import (
    annotate_points,
    fixedtime_df,
    team_coord
)
from triple_triple.full_court import draw_court
from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_df_raw_position_data, 
    get_df_positions
)

# TODO: Fix legend in plot_play_snap_shot

df_positions = get_df_positions()
df_raw_position_data = get_df_raw_position_data()

# display x amount of rows in dataframe:            
# with pd.option_context('display.max_rows', 200):
    # print df_raw_position_data
            

# Plot ONE player during a fixed time range
def plot_player_movement_gradient(player, period, time_start, time_end, 
    color='winter', dataframe=df_raw_position_data):
    
    player_fixed_time = dataframe[(dataframe.player_name == player) & 
                        (dataframe.period == period) &
                        (dataframe.game_clock <= time_start) &
                        (dataframe.game_clock >= time_end)]
    
    n = len(player_fixed_time)
    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    ax.scatter(player_fixed_time.x_loc.head(n), 
                player_fixed_time.y_loc.head(n), 
                c = player_fixed_time.game_clock.head(n), 
                cmap = color, s=400, zorder=1)

    # Label coordinates:
    x = player_fixed_time.iloc[n-1]['x_loc']
    y = player_fixed_time.iloc[n-1]['y_loc']
    text = player_fixed_time.iloc[0]['player_jersey']               
    label = ax.annotate(text, xy = (x - .6, y - .4))
    
    plt.show()
    
# Plot TEAM during time range
def plot_play_snap_shot(period, time_start, time_end, 
    hometeam_id, awayteam_id, title_text):

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax) 
    
    df_fixedtime = fixedtime_df(period, time_start, time_end, df_positions)
  
    # initial coordinates:
    # players
    x_home, y_home, player_home = team_coord(0, hometeam_id, df_fixedtime)
    x_away, y_away, player_away = team_coord(0, awayteam_id, df_fixedtime)
    
    # iniial ball coordinates (all we care about)
    x_ball, y_ball, ball_id = team_coord(0, -1, df_fixedtime)
    
    # plot the initial point    
    scat_home = ax.scatter(x_home, y_home, color='blue', s=400, 
                label='Golden State Warriors') 
    scat_away = ax.scatter(x_away, y_away, color ='red', s=400,
                label='Miami Heat')
    scat_ball = ax.scatter(x_ball, y_ball, color='black', s=400, label='ball')
                
    # Label the coordinates
    home_annotations = annotate_points(ax, x_home, y_home, player_home)
    away_annotations = annotate_points(ax, x_away, y_away, player_away)
                
    plt.title(title_text)
    plt.legend(loc='lower left')
    #fig.savefig('play_snap_shot.png') 
                
    plt.show()
######################
######################
if __name__ == '__main__':
               
    player = 'Dwyane Wade'
    period = 1
    time_start = 402
    time_end = 400
    
    plot_player_movement_gradient(player, period, time_start, time_end, 
        dataframe=df_raw_position_data, color='Blues')

    ######################
    period = 2
    time_start = 100
    time_end = 99
    title_text = 'Snap shot of MIA @ GSW \n January 11, 2016' 
    
    plot_play_snap_shot(period, time_start, time_end, 
        hometeam_id,  awayteam_id, title_text)
