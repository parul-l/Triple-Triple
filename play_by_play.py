import requests
import json
from collections import OrderedDict
import datetime
import pandas as pd
import matplotlib as plt
from matplotlib import animation

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
           'referer': 'http://stats.nba.com/team/'
          }

def get_data(url, headers=HEADERS):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)

# January 11, 2016, MIA @ GSW        
url = "http://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID=0021500568&RangeType=2&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0"        

play_data = get_data(url)

def time_in_seconds(time):
    t = time.split(':')
    return int(t[0])*60 + int(t[1])

def score_in_int(score):
    try: 
        new_score = [int(score.split('-')[0]),
        int(score.split('-')[1])]
        return new_score     
    
    except:
        new_score = score
        return new_score      
      
headers = ["Game_ID",
            "PERIOD",
            "WCTIMESTRING",
            "PCTIMESTRING",
            "HOMEDESCRIPTION",
            "NEUTRAL DESCRIPTION",
            "VISITORDESCRIPTION",
            "SCORE",  #[Away, Home]
            "PLAYER1_ID",
            "PLAYER1_NAME",
            "PLAYER2_ID",
            "PLAYER2_NAME",
            "PLAYER3_ID",
            "PLAYER3_NAME"
        ]      

play_by_play = []        
len_plays = len(play_data['resultSets'][0]['rowSet'])

for i in range(len_plays):
    play_by_play.append(
    [
    play_data['resultSets'][0]['rowSet'][i][0],
    play_data['resultSets'][0]['rowSet'][i][4],
    play_data['resultSets'][0]['rowSet'][i][5],
    time_in_seconds(play_data['resultSets'][0]['rowSet'][i][6]),
    play_data['resultSets'][0]['rowSet'][i][7],
    play_data['resultSets'][0]['rowSet'][i][8],
    play_data['resultSets'][0]['rowSet'][i][9],
    score_in_int(play_data['resultSets'][0]['rowSet'][i][10]),
    play_data['resultSets'][0]['rowSet'][i][13],
    play_data['resultSets'][0]['rowSet'][i][14],
    play_data['resultSets'][0]['rowSet'][i][20],
    play_data['resultSets'][0]['rowSet'][i][21],
    play_data['resultSets'][0]['rowSet'][i][27],
    play_data['resultSets'][0]['rowSet'][i][28]
    ])
    
# create a data frame from the list
df_play = pd.DataFrame(play_by_play, columns = headers)    

# Collect times where shots were made
play_scored = []

for item in play_by_play:
    if type(item[7]) == list:
        play_scored.append(item)

# Collect Wade shots:
wade_shots = []
for item in play_scored:
    if item[9] =='Dwyane Wade':
        wade_shots.append(item)

# Determie all players on court at Wade's 0th shot
def all_players_at_shot_time(period, time): 
    return df[ (df.period == period) &
            (df.game_clock - time< 1) &
            (df.game_clock - time>=0)]

# Track players at Wade's 0th shot
def plot_shot_times(player, period, time, color):
    player_shot_time = df[(df.player_name == player) & 
                        (df.period == period) &
                        (df.game_clock - time < 1) &(df.game_clock - time>=0)]
    
    n = len(player_shot_time)
    plt.scatter(player_shot_time.x_loc.head(n), player_shot_time.y_loc.head(n), 
                c = player_shot_time.game_clock.head(n), 
                cmap = color, s=400, zorder=1)

    # Label coordinates:
    x = player_shot_time.iloc[n-1]['x_loc']
    y = player_shot_time.iloc[n-1]['y_loc']
    text = player_shot_time.iloc[0]['player_jersey']               
    label = ax.annotate(text, xy = (x-.6, y-.4))

# Plot all players on the court for each of Wade's shots:
# These are still figures (not animations)
for k in range(1,2):
    fig = plt.figure(figsize=(15,9))
    ax = draw_court()
    period = wade_shots[k][1]
    time = wade_shots[k][3]
    
    apst = all_players_at_shot_time(period, time)
    
    for i in range(1, 11):
        player  = apst['player_name'].iloc[i]
        period  = wade_shots[k][1]
        time    = apst['game_clock'].iloc[i]
        
        if apst['team_id'].iloc[i] == 1610612744:
            color = plt.cm.Blues
            
        elif apst['team_id'].iloc[i] == 1610612748:
            color = plt.cm.OrRd    
            
        plot_shot_times(player, period, time, color)
   
########################
#######################
df_wade = df_positions[['period', 'game_clock', 'Dwyane Wade', 'ball']]
df_wade = df_wade[df_wade['Dwyane Wade']!= (-10, -10)]

dist = []
for i in range(len(df_wade)):
    dist.append(np.linalg.norm
    (np.array(df_wade[df_wade.columns[2]].iloc[i])-
    np.array(df_wade[df_wade.columns[3]].iloc[i])))

df_wade['dist_ball'] = dist

df_wade_has_ball = df_wade[df_wade['dist_ball'] <=1]

# get the full second that he has the ball
time = np.array(df_wade_has_ball['game_clock'])
rounded_clock = []

for item in time:
    rounded_clock.append(int(item))

df_wade_has_ball['rounded_clock'] = rounded_clock
df_wade_has_ball_rounded= df_wade_has_ball.loc[df_wade_has_ball.groupby
                (['period', 'rounded_clock'])['rounded_clock'].idxmax()]

def player_region_time(df, player):
    list_region = []
    for i in range(len(df)):
        reg = region(df[player].iloc[i][0], df[player].iloc[i][1])
        list_region.append(reg)
    return list_region


region_before = player_region_time(df_wade_has_ball_rounded, 'Dwyane Wade')



region_after_4sec = []

# This gives a dataframe of one or two rows of a player and the ball
# at a small, specific time 
def get_player_ball(df_positions, period, game_clock, player):
    df_positions_trunc = df_positions[
                    (df_positions['period']==period) & 
                    (df_positions['game_clock'] <= game_clock) & 
                    (df_positions['game_clock'] >= game_clock-0.04)]
    return df_positions_trunc[['period', 'game_clock', player, 'ball']]                

region_after_player = []
region_after_ball = []
has_ball = []
period_play = []
game_clock_before = []
game_clock_after = []
no_touches = len(df_wade_has_ball_rounded)

for i in range(no_touches):
    try:
        time = df_wade_has_ball_rounded['rounded_clock'].iloc[i]
        game_clock = time - 5
        period = df_wade_has_ball_rounded['period'].iloc[i]
        player = 'Dwyane Wade'
        df_wade_next = get_player_ball(df_positions, period, game_clock, player)
        
        # create columns of game clock
        game_clock_before.append(time)
        game_clock_after.append(game_clock)
        period_play.append(period)
        
        # take only positions at first first row and
        # determine the region of ball and player
        player_pos = df_wade_next[:1][player].iloc[0]
        ball_pos = df_wade_next[:1]['ball'].iloc[0]
        
        reg_player = region(player_pos[0], player_pos[1])
        reg_ball = region(ball_pos[0], ball_pos[1])
        region_after_player.append(reg_player)
        region_after_ball.append(reg_ball)
        
        # determine if player has ball
        has_ball.append(player_has_ball(player_pos[0], player_pos[1],ball_pos[0], ball_pos[1]))
    except:
        region_after_player.append('')
        region_after_ball.append('')
        has_ball.append('')


d = {'period': period,
    'game_clock_before': game_clock_before,
    'game_clock_after': game_clock_after,
    'reg_player_before': region_before,
    'reg_player_after': region_after_player,
    'reg_ball_after': region_after_ball,
    'has_ball': has_ball} 
    
df_regions = pd.DataFrame(d, columns = d.keys())     

# collect all of Wade's impact     
df_play_wade = df_play[(df_play['PLAYER1_NAME']=='Dwyane Wade')|
                        (df_play['PLAYER2_NAME']=='Dwyane Wade')|
                        (df_play['PLAYER3_NAME']=='Dwyane Wade')

wade_impact = []
                        
for i in range(len(df_play_wade)):
    try:
        if (df_play_wade['VISITORDESCRIPTION'].iloc[i].startswith('Wade') or df_play_wade['VISITORDESCRIPTION'].iloc[i].startswith('MISS')):
            wade_impact.append([df_play_wade['PERIOD'].iloc[i], df_play_wade['PCTIMESTRING'].iloc[i], df_play_wade['VISITORDESCRIPTION'].iloc[i]])         
    except:
        print i

print wade_impact       

shot_attempt = 0
rebound_count = 0
foul_count = 0
free_throw = 0
blocks = 0

for item in wade_impact:
    if item[2].startswith('Wade REBOUND'):
        rebound_count +=1
    elif item[2].startswith('MISS '):
        shot_attempt +=1
    elif item[2].startswith('Wade BLOCK'):
        blocks +=1
    elif item[2].startswith('Wade S.FOUL'):
        foul_count +=1
    elif item[2].startswith('Wade Free Throw'):
        free_throw +=1
    else:
        shot_attempt +=1        

#######################
#######################
# Histogram plot of percentages
######################
######################    

# Number of total touches. Assuming each touch is about 4 seconds
touches = len(df_wade_has_ball_rounded) /4.
shot_perc = shot_attempt/touches
reb_perc = rebound_count/touches
foul_perc = foul_count/touches
free_throw_perc = free_throw/touches
blocks_perc = blocks/touches
passes_perc = (touches - shot_attempt - 
            free_throw - rebound_count -foul_count - blocks)/touches

data_plot = [shot_perc, reb_perc, foul_perc, 
            free_throw_perc, blocks_perc, passes_perc]

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

N=6
# x location of bars, and their width
ind = np.arange(N)  
width = 0.35

d = ax.bar(ind, data_plot, width, color = 'red')

ax.set_xlim(-width, len(ind) + width)
ax.set_ylim(0, 0.5)
ax.set_ylabel('Fraction of Touches')
ax.set_title('Dwyane Wade Ball Touch Distribution (@ GSW) \n January 11, 2016')
xTickMarks = ['Shot Attempts', 'Rebounds', 'Fouls', 'Free Throws', 
            'Blocks', 'Passes']
ax.set_xticks(ind)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)            

fig.savefig('wade_touches.png')
plt.show()





for i in range(len(df_play_wade)):
    try:
        if 'turnover' in df_play_wade['VISITORDESCRIPTION'].iloc[i]:
            print df_play_wade['VISITORDESCRIPTION'].iloc[i]
    except:
        print i              

    
