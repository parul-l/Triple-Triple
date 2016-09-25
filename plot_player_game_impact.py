import matplotlib.pyplot as plt

# Don't think I'm importing these correctly
from play_by_play_nbastats import df_play_by_play
from play_by_play_nbastats import teams_playing
# from player_passing_habits import closest_to_ball


# NBA STATS DESCRIPTION
# PLAYER 1: commit foul, shoot, turnover, rebound, free throws, jump ball, sub
# PLAYER 2: assist, player is fouled (no description), steals, jump ball, sub
# PLAYER 3: block, jump ball is tipped to player

def playerid_from_name(player, player_info_dict=game_id_dict):
    for key, value in game_id_dict.items():
        if value[0]==player:
            return key

player = 'Chris Bosh'
game_id = '0021500568'
home_team, away_team = teams_playing(game_id)            
playerid = playerid_from_name(player)
player_lastname = game_id_dict[playerid][0].split()[1]

def player_impact(playerid, dataframe=df_play_by_play):
    playerid = int(playerid)
    df_pbp_player = dataframe[
                             (dataframe['PLAYER1_ID']==playerid)|           (dataframe['PLAYER2_ID']==playerid)|           (dataframe['PLAYER3_ID']==playerid)]

                             
    if df_pbp_player.iloc[0]['PLAYER1_ID']==playerid:
        if df_pbp_player.iloc[0]['PLAYER1_TEAM_ID']==home_team:
            descrip='HOMEDESCRIPTION'
        else:
            descrip='VISITORDESCRIPTION' 
                
    elif df_pbp_player.iloc[0]['PLAYER2_ID']==playerid:
        if df_pbp_player.iloc[0]['PLAYER2_TEAM_ID']==home_team:
            descrip='HOMEDESCRIPTION'
        else:
            descrip='VISITORDESCRIPTION' 
    elif df_pbp_player.iloc[0]['PLAYER3_ID']==playerid:
        if df_pbp_player.iloc[0]['PLAYER3_TEAM_ID']==home_team:
            descrip='HOMEDESCRIPTION'
        else:
            descrip='VISITORDESCRIPTION'
    
    # drop NaN descriptions (=player is fouled)        
    df_pbp_player = df_pbp_player[pd.notnull(df_pbp_player[descrip])]
    df_pbp_player = df_pbp_player.reset_index()
    df_player_impact = df_pbp_player[['PERIOD', 'PCTIMESTRING',
    descrip]]

    return df_player_impact 

player = 'Chris Bosh'
playerid = playerid_from_name(player)
df_player_impact = player_impact(playerid)

def player_game_info_nba(playerid, dataframe = df_player_impact):
    assist = []
    turnover = []
    free_throw = []
    rebound = []
    commit_foul = []    
    block = []
    steal = []  
    shoot = []      

    player_lastname = game_id_dict[playerid][0].split()[1]
        
    for i in range(len(dataframe)):
        descrip_split =  dataframe.ix[:,2].iloc[i].split()
        if (descrip_split[-3]=='('+ player_lastname and
            descrip_split[-1]=='AST)'):
            assist.append([dataframe.iloc[i]['PERIOD'],
                           dataframe.iloc[i]['PCTIMESTRING'],
                           dataframe.ix[:,2].iloc[i]])
        
        elif 'Turnover' in dataframe.ix[:,2].iloc[i]:
            turnover.append([dataframe.iloc[i]['PERIOD'],
                           dataframe.iloc[i]['PCTIMESTRING'],
                           dataframe.ix[:,2].iloc[i]])
        
        elif (descrip_split[0]==player_lastname and 
              descrip_split[1]=='Free' and
              descrip_split[2]=='Throw'):
            free_throw.append([dataframe.iloc[i]['PERIOD'],
                             dataframe.iloc[i]['PCTIMESTRING'],
                             dataframe.ix[:,2].iloc[i]])
                             
        elif (descrip_split[0]==player_lastname and 
              descrip_split[1]=='REBOUND'):
            rebound.append([dataframe.iloc[i]['PERIOD'],
                            dataframe.iloc[i]['PCTIMESTRING'],
                            dataframe.ix[:,2].iloc[i]])
        elif (descrip_split[0]==player_lastname and 
              descrip_split[1]=='STEAL'):
            steal.append([dataframe.iloc[i]['PERIOD'],
                            dataframe.iloc[i]['PCTIMESTRING'],
                            dataframe.ix[:,2].iloc[i]])
        elif (descrip_split[0]==player_lastname and 
              descrip_split[1]=='BLOCK'):
            block.append([dataframe.iloc[i]['PERIOD'],
                            dataframe.iloc[i]['PCTIMESTRING'],
                            dataframe.ix[:,2].iloc[i]])          
        elif (descrip_split[0]==player_lastname and 
              'FOUL' in descrip_split[1]):
            commit_foul.append([dataframe.iloc[i]['PERIOD'],
                            dataframe.iloc[i]['PCTIMESTRING'],
                            dataframe.ix[:,2].iloc[i]])         
        elif ((descrip_split[0]=='MISS' and 'Free Throw' not in     
              dataframe.ix[:,2].iloc[i] )  
              or  
             (descrip_split[0]==player_lastname and 
              'PTS' in dataframe.ix[:,2].iloc[i] and
              'Free Throw' not in dataframe.ix[:,2].iloc[i])):
            shoot.append([dataframe.iloc[i]['PERIOD'],
                            dataframe.iloc[i]['PCTIMESTRING'],
                            dataframe.ix[:,2].iloc[i]])                                   
    return assist, turnover, free_throw, rebound, commit_foul, block, steal, shoot



player = 'Chris Bosh'
game_id = '0021500568'
home_team, away_team = teams_playing(game_id) 
playerid = playerid_from_name(player)
df_player_impact = player_impact(playerid)
assist, turnover, free_throw, rebound, commit_foul, block, steal, shoot = player_game_info_nba(playerid)

def plot_player_game_info(playerid):
    assist, turnover, free_throw, rebound, commit_foul, block, steal, shoot = player_game_info_nba(playerid)

    df_dist_to_ball = closest_to_ball()
    df_player = df_dist_to_ball[df_dist_to_ball['closest_player']==player]
    
    # Number of total touches. Assuming each touch is about 3 seconds
    # Data given 25 frames per second
    touches = len(df_player) /75.
    shot_attempt = len(shoot)
    rebound_count = len(rebound)
    foul_count = len(commit_foul)
    free_throw_attempt = len(free_throw)
    blocks = len(block)
    turnovers = len(turnover)
    
    passes = touches - shot_attempt - free_throw_attempt - rebound_count -foul_count - blocks-turnovers        
    
    #######################
    # Histogram plot of percentages
    ######################
    shot_perc = shot_attempt/touches
    reb_perc = rebound_count/touches
    foul_perc = foul_count/touches
    free_throw_perc = free_throw_attempt/touches
    blocks_perc = blocks/touches
    turnovers_perc = turnovers/touches
    passes_perc = passes/touches
    
    data_plot = [shot_perc, reb_perc, foul_perc, free_throw_perc, blocks_perc, 
                turnovers_perc, passes_perc]
        
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    
    N=len(data_plot)
    # x location of bars, and their width
    ind = np.arange(N)  
    width = 0.35
    
    d = ax.bar(ind, data_plot, width, color = 'red')
    
    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylim(0, 0.5)
    ax.set_ylabel('Fraction of Touches')
    ax.set_title(player + ' Ball Touch Distribution (@ GSW) \n January 11,2016')
    xTickMarks = ['Shot Attempts', 'Rebounds', 'Fouls', 'Free Throws', 
                'Blocks', 'Turnovers', 'Passes']
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)            
        
    # fig.savefig('player_touches.png')
    plt.show()

    return "Touches=" + str(touches) + " ShotAttempts=" + str(shot_attempt) + " Rebounds=" + str(rebound_count) + " FoulCount=" + str(foul_count) + " FreeThrowAttempts=" + str(free_throw_attempt) + " Blocks=" + str(blocks) + " Turnovers=" + str(turnovers) + " Passes=" + str(passes)
                        
plot_player_game_info(playerid) 
