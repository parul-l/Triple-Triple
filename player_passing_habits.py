def dist_two_points(p1,p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2)  

# dataframe of specific player and ball positions and 
# distance from ball  
# this doesn't work if player = ball since 'ball' column is already
# called when we create the df                
def player_dist_to_ball_df(player, dataframe=df_positions):   
    df_player = dataframe[['period', 'game_clock', player,'ball']]
    df_player = df_player[df_player[player]['x_loc']!= -10]

    # Add distance-to-ball and player regions column
    player_coord =  np.array(df_player[player])
    ball_coord =    np.array(df_player['ball'])

    dist_to_ball = []
    player_region = []
    for i in range(len(df_player)):
        dist_to_ball.append(dist_two_points(player_coord[i], ball_coord[i]))
        player_region.append(region(player_coord[i][0], player_coord[i][1]))

    df_player['dist_ball'] = dist_to_ball
    df_player['region'] = player_region
    
    return df_player
       
# Determine who is closest two players to ball at every moment #
# TODO: Combine closest_to_ball and pos_and_dist functions to one df
# with player coords and distances
#############################
def closest_to_ball(dataframe=df_positions):
    df_pos_x_loc = dataframe.iloc[:,dataframe.columns.get_level_values(1)=='x_loc'] 
    df_pos_y_loc = dataframe.iloc[:,dataframe.columns.get_level_values(1)=='y_loc']
    
    dist_x = (df_pos_x_loc.values.T - dataframe['ball']['x_loc'].values)**2
    dist_y = (df_pos_y_loc.values.T - dataframe['ball']['y_loc'].values)**2
    
    dist_to_ball = np.sqrt(dist_x + dist_y)
    
    # get column headers = player list 
    # (Note: df_positions.columns.levels[0] doesn't preserve the order of the columns)
    player_list= list(df_pos_x_loc) 
    player_list = map(lambda x: x[0], player_list)
    # append distances to df_positions
    # there must be a better way to do this
    for i in range(len(player_list)):
        df_positions[player_list[i], 'dist'] = dist_to_ball[i]
    df_positions = df_positions.sort_index(axis=1)
    
    # Remove ball column to get player relative distances
    df_positions = df_positions.drop('ball', axis=1)
    
    # TODO: FIND CLOSEST PLAYERS#    
    
    # makedataframe
    df_dist_to_ball = pd.DataFrame(dist_to_ball.T, columns = player_list)
    
    # Remove ball column to get player relative distances
    df_dist_to_ball = df_dist_to_ball[player_list[:-1]]
    
    # get closest two players
    pos_matrix = df_dist_to_ball.values
    # np.argpartition(matrix, 2lowest, rows) gives an array of order
    # For max values, write -2, I think
    idx_sorted = np.argpartition(pos_matrix, 2, axis=1)
    pos_matrix_sorted = np.partition(pos_matrix, 2, axis=1)
    # [:,[0, 1, 2]] say, gives all rows and columns 0, 1, and 2
    idx_low = idx_sorted[:,0] 
    idx_second_low = idx_sorted[:,1]

    second_closest_values = pos_matrix_sorted[:, 1]
    
    closest_player = []
    second_closest_player = []
    for i in range(len(idx_low)):
        closest_player.append(player_list[idx_low[i]])
        second_closest_player.append(player_list[idx_second_low[i]])
        
    # Append two lowest distances and the players    
    
    df_dist_to_ball['min_dist'] = df_dist_to_ball.loc[:, player_list[:-1]].min(axis=1)
    df_dist_to_ball['closest_player'] = closest_player
    
    df_dist_to_ball['second_min'] = second_closest_values
    df_dist_to_ball['second_closest_player'] = second_closest_player
    
    # add period and game_clock
    df_dist_to_ball['period'] = np.array(dataframe['period']['period'])
    df_dist_to_ball['game_clock'] = np.array(dataframe['game_clock']['game_clock'])
    
    return df_dist_to_ball

def pos_and_dist(dataframe=df_positions):
    df_dist_to_ball = closest_to_ball()
    # Add closest players to position dataframe
    df_positions['min_dist'] = df_dist_to_ball['min_dist'].values
    df_positions['closest_to_ball'] = df_dist_to_ball['closest_player'].values
    df_positions['second_min'] = df_dist_to_ball['second_min'].values
    df_positions['second_closest_player'] = df_dist_to_ball['second_closest_player'].values
    
    return df_positions
    

def player_closest_to_ball(player, dataframe=df_positions):
    df_pos_dist = pos_and_dist()
    # or add this after to get when player is close to ball
    df_pos_dist = df_pos_dist[df_pos_dist.min_dist <=2]
    df_pos_dist = df_pos_dist.reset_index()
    closest_player_to_ball = df_pos_dist['closest_to_ball'].values
        
    player_ball = [None]*len(closest_player_to_ball)
    ball_after_player = [None]*len(closest_player_to_ball)
    
    player_ball_idx = []
    ball_after_player_idx = []
    
    for i in range(len(closest_player_to_ball)):
        if (closest_player_to_ball[i]==player and closest_player_to_ball[i-1] != player):
            player_ball[i] = player
            player_ball_idx.append(i)
        elif (closest_player_to_ball[i]!=player and closest_player_to_ball[i-1]==player):
            ball_after_player[i] = closest_player_to_ball[i]
            ball_after_player_idx.append(i)
    
    return player_ball, ball_after_player, player_ball_idx, ball_after_player_idx

def characterize_play(player_ball_idx, ball_after_player_idx, 
                     shoot, assist, turnover):

    play_shot = []
    play_assist = []
    play_turnover = []
    start_idx_used = []   
    end_idx_used = []
    
    for j in range(len(player_ball_idx)):
        # Start of play
        play_start_index = player_ball_idx[j]
        period_play_start = df_pos_dist_trunc.period.period.iloc[play_start_index]
        game_clock_play_start = df_pos_dist_trunc.game_clock.game_clock.iloc[play_start_index]
        
        side = team_shooting_side(player, period_play_start, shooting_side, hometeam_id, awayteam_id) 

        start_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_start_index],df_pos_dist_trunc[player].y_loc.iloc[play_start_index], side)

        # End of play      
        play_end_index = ball_after_player_idx[j]-1
        game_clock_play_end = df_pos_dist_trunc.game_clock.game_clock.iloc[play_end_index]
        
        end_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_end_index],df_pos_dist_trunc[player].y_loc.iloc[play_end_index], side)
        
        # check if possession is shot, turnover, assist 
        # shot (assuming about 4 seconds to get to rim?)
        for i in range(len(shoot)):
            if (shoot[i][0]== period_play_start and
                0<= game_clock_play_end-shoot[i][1] < 4):
                play_shot.append([
                period_play_start,
                game_clock_play_end,
                start_region,
                end_region,
                'shot'])
                
                start_idx_used.append(play_start_index)
                # add +1 to account for play_end_index
                end_idx_used.append(play_end_index+1)
                
        # assist (assuming 6 seconds in between pass and shot)    
        for i in range(len(assist)):
            if (assist[i][0]==period_play_start and
                0<= game_clock_play_end-assist[i][1] < 6):
                play_assist.append([
                period_play_start,
                game_clock_play_end,
                start_region,
                end_region,
                'assist'])
                
                start_idx_used.append(play_start_index)
                end_idx_used.append(play_end_index+1)
                
        #turnover (assuming 2 seconds between touch and turnover)
        for i in range(len(turnover)):
            if (turnover[i][0]==period_play_start and
                0<= game_clock_play_end-turnover[i][1] < 2):
                play_turnover.append([
                period_play_start,
                game_clock_play_end,
                start_region,
                end_region,
                'turnover'])

                start_idx_used.append(play_start_index)
                end_idx_used.append(play_end_index+1)

    return play_shot, play_assist, play_turnover, start_idx_used, end_idx_used


def team_id_from_name(name):
    for value in game_id_dict.values():
        if value[0]==name:
            return value[2]    

def closest_player_team_ids(dataframe = df_positions):  
    df_pos_dist = pos_and_dist()
    # or add this after to get when player is close to ball
    df_pos_dist = df_pos_dist[df_pos_dist.min_dist <=2]
    closest_player_to_ball = df_pos_dist['closest_to_ball'].values
    
    closest_player_team = []
    for item in closest_player_to_ball:
        closest_player_team.append(
        team_id_from_name(item)
        )
    return closest_player_team 
    
# probably should contain a lot of arguments
# t= 25 corresponds to 1 sec
# only consider 'possessions' when player has ball for more
# than t seconds?
def pass_not_assist(player_ball_idx, ball_after_player_idx, start_idx_used, end_idx_used, t=10):

    # collect possession indices

    length_possession = np.array(ball_after_player_idx)-np.array(player_ball_idx)
    possession = np.argwhere(length_possession <t)
    possession = possession.flatten()
    
    player_ball_idx = np.delete(np.array(player_ball_idx), possession)
    ball_after_player_idx = np.delete(np.array(ball_after_player_idx), possession)
    
    start_idx_used = np.delete(np.array(start_idx_used), possession)
    end_idx_used = np.delete(np.array(end_idx_used), possession)
    # collect the discrepancies between the nba sets and my sets and order them
    
    start_idx_not_used = sorted(list(set(player_ball_idx)-set(start_idx_used)))
    end_idx_not_used =   sorted(list(set(ball_after_player_idx)-set(end_idx_used)))           
    play_pass = []       
    player_team_id = team_id_from_name(player)
    closest_players = df_pos_dist_trunc.closest_to_ball.values
    closest_player_team = closest_player_team_ids()

    for i in range(len(start_idx_not_used)):
        play_start_index = start_idx_not_used[i]
        play_end_index = end_idx_not_used[i]-1
        # end of player possession
        end_possession_idx = end_idx_not_used[i]
        # find next time same team has ball
        # first start the list at the end index (now index =0)
        # find index of same team and add it back original index  

        next_team_idx = next(closest_player_team[end_possession_idx:].index(i) for i in closest_player_team[end_possession_idx:] if i == player_team_id) + end_possession_idx

        # determine who the player is
        next_teammate = closest_players[next_team_idx]

        # if next_teammate ==player, just ignore it
        # either stoppage of play or something is funny

        if next_teammate != player:
            # check the next t indices are the same player
            # corresponding to a possession
            # if true, record it as a pass
            if len(set(closest_players[next_team_idx:next_team_idx+t]))==1:
                period_play_start = df_pos_dist_trunc.period.period.iloc[play_start_index]
                game_clock_play_start = df_pos_dist_trunc.game_clock.game_clock.iloc[play_start_index]
                
                side = team_shooting_side(player, period_play_start, shooting_side, hometeam_id, awayteam_id) 

                start_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_start_index],df_pos_dist_trunc[player].y_loc.iloc[play_start_index], side)

                # End of play
                # Index where ball ends up      
                game_clock_play_end = df_pos_dist_trunc.game_clock.game_clock.iloc[next_team_idx]

                end_region = region(df_pos_dist_trunc[next_teammate].x_loc.iloc[next_team_idx],df_pos_dist_trunc[next_teammate].y_loc.iloc[next_team_idx],side)

                play_pass.append([
                period_play_start,
                game_clock_play_end,
                start_region,
                end_region,
                'pass'])
    return play_pass
    
def plot_team_possession(closest_player_team,start, stop, hometeam_id, awayteam_id):
    closest_player_team =closest_player_team[start:stop]
    x_home = [] 
    x_away = []
    for i in range(len(closest_player_team)):
        if closest_player_team[i] == hometeam_id:
            x_home.append(i+start)             
        elif closest_player_team[i] == awayteam_id:
            x_away.append(i+start) 
            
    y_home = [0]*(len(x_home))          
    y_away =[1]*(len(x_away))
              
    fig = plt.figure()
    ax = fig.gca()
    plt.xlim(start,stop)
    plt.ylim(0, 2)
    ax.scatter(x_home, y_home, color = 'blue', s=30)
    ax.scatter(x_away, y_away, color = 'red', s=30)
    plt.show()
    
    return x_home, y_home, x_away, y_away      

##################################                  
##################################        
import numpy as np
import math
from court_regions import region
import team_shooting_side

game_id = '0021500568'
home_team, away_team = teams_playing(game_id) 
# then get df_positions for that game

    
player = 'Chris Bosh'
hometeam_id = '1610612744'
awayteam_id = '1610612748'

df_dist_to_ball = closest_to_ball()

df_pos_dist = pos_and_dist(dataframe=df_positions)
df_pos_dist_trunc = df_pos_dist[df_pos_dist.min_dist <=2]
df_pos_dist_trunc = df_pos_dist_trunc.reset_index()
player_ball, ball_after_player, player_ball_idx, ball_after_player_idx  = player_closest_to_ball(player, dataframe=df_positions)

closest_player_team = closest_player_team_ids()

play_shot, play_assist, play_turnover, start_idx_used, end_idx_used = characterize_play(player_ball_idx, ball_after_player_idx, shoot, assist, turnover)

play_pass = pass_not_assist(player_ball_idx, ball_after_player_idx, start_idx_used, end_idx_used, t=10)




x_home, y_home, x_away, y_away = plot_team_possession(closest_player_team, 360, 460, hometeam_id, awayteam_id)





#################
idx_start = player_ball_idx[140]
idx_end = ball_after_player_idx[140]
playerid = playerid_from_name(player)
player_team = game_id_dict[playerid][2]






# plot using play_animation     

hometeam_id = '1610612744'
awayteam_id = '1610612748'
idx_start = player_ball_idx[1]
idx_end = ball_after_player_idx[1]
period = df_pos_dist.period.period.iloc[idx_start]
time_start = df_pos_dist.game_clock.game_clock.iloc[idx_start]
time_end = df_pos_dist.game_clock.game_clock.iloc[idx_end]  

hometeam_id = '1610612744'
awayteam_id = '1610612748'
period = 1
time_start = 407
time_end = 401


fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
anim = play_animation(df_positions, fig= fig, period = period, time_start = time_start, time_end =time_end, hometeam_id = hometeam_id, awayteam_id = awayteam_id)
#anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
plt.show()
plt.ioff()  
