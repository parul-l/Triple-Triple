
play_shot = []
play_pass = []
play_turnover = []
start_idx_used = []   
end_idx_used = []
    
for j in range(len(player_ball_idx)):
    play_start_index = player_ball_idx[j]
    period_play_start = df_pos_dist_trunc.period.period.iloc[play_start_index]
    game_clock_play_start = df_pos_dist_trunc.game_clock.game_clock.iloc[play_start_index]

    start_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_start_index],  
           df_pos_dist_trunc[player].y_loc.iloc[play_start_index])

    # quarter, time, and region that ends player with ball       
    play_end_index = ball_after_player_idx[j]-1
    game_clock_play_end = df_pos_dist_trunc.game_clock.game_clock.iloc[play_end_index]

    end_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_end_index],  
           df_pos_dist_trunc[player].y_loc.iloc[play_end_index])
    
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
            play_pass.append([
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



            
# collect the discrepancies between the sets and order them
start_idx_not_used = sorted(list(set(player_ball_idx)-set(start_idx_used)))
end_idx_not_used =   sorted(list(set(ball_after_player_idx)-set(end_idx_used)))          

play_pass = []
idx_number = 3
player_team_id = team_id_from_name(player)
closest_players = df_pos_dist_trunc.closest_to_ball.values
closest_player_team = closest_player_team_ids()

for i in range(len(start_idx_not_used)):
    idx_number = i
    play_start_index = start_idx_not_used[idx_number]
    play_end_index = end_idx_not_used[idx_number]-1
    # end of player possession
    end_possession_idx = end_idx_not_used[idx_number]
    # find next time same team has ball
    # first start the list at the end index (now index =0)
    # find index of same team and add it back original index  

    next_team_idx = next(closest_player_team[end_possession_idx:].index(i) for i in closest_player_team[end_possession_idx:] if i == player_team_id) + end_possession_idx

    # determine who the player is
    next_teammate = closest_players[next_team_idx]

    # if next_teammate ==player, just ignore it
    # either stoppage of play or something is funny

    if next_teammate != player:
        # check the next three indices are the same player
        # if true, record it as a pass
        if len(set(closest[next_team_idx:next_team_idx+4]))==1:
            period_play_start = df_pos_dist_trunc.period.period.iloc[play_start_index]
            game_clock_play_start = df_pos_dist_trunc.game_clock.game_clock.iloc[play_start_index]

            start_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_start_index],df_pos_dist_trunc[player].y_loc.iloc[play_start_index])

            # End of play      
            game_clock_play_end = df_pos_dist_trunc.game_clock.game_clock.iloc[play_end_index]

            end_region = region(df_pos_dist_trunc[player].x_loc.iloc[play_end_index],df_pos_dist_trunc[player].y_loc.iloc[play_end_index])

            play_pass.append([
            period_play_start,
            game_clock_play_end,
            start_region,
            end_region,
            'pass'])








hometeam_id = '1610612744'
awayteam_id = '1610612748'
idx_number = 3
play_start_index = start_idx_not_used[idx_number]
play_end_index = end_idx_not_used[idx_number]-1
period = df_pos_dist_trunc.period.period.iloc[play_start_index]
time_start = df_pos_dist_trunc.game_clock.game_clock.iloc[play_start_index]
time_end = df_pos_dist_trunc.game_clock.game_clock.iloc[play_end_index]

# There is a glitch with these times, quarter 1 
period = 1
time_start = 707
time_end = 702

fig = plt.figure(figsize=(15, 9))
ax = fig.gca()
ax = draw_court(ax)
anim = play_animation(df_positions, fig= fig, period = period, time_start = time_start, time_end =time_end, hometeam_id = hometeam_id, awayteam_id = awayteam_id)
#anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
plt.show()
plt.ioff()  




df_test  = df_pos_dist[(df_pos_dist.period.period==1)&(df_pos_dist.game_clock.game_clock<=407) & (df_pos_dist.game_clock.game_clock>=293)&
(df_pos_dist.closest_to_ball==player)] 

df_test_trunc  = df_pos_dist_trunc[(df_pos_dist_trunc.period.period==2)&(df_pos_dist_trunc.game_clock.game_clock<=311) & (df_pos_dist_trunc.game_clock.game_clock>=307)&
(df_pos_dist_trunc.closest_to_ball==player)] 

df_dist_to_ball[(df_dist_to_ball.period==1)&(df_dist_to_ball.game_clock<=698) & (df_dist_to_ball.game_clock>=697)]['Chris Bosh']


# find index of first score
score = list(df_play_by_play.SCORE.values)
first_score_idx = next(score.index(item) for item in score if type(item)==list)
# find position 
first_score_period = df_play_by_play.PERIOD.iloc[first_score_idx]
first_score_game_clock = df_play_by_play.PCTIMESTRING.iloc[first_score_idx]
first_score_player = df_play_by_play.PLAYER1_NAME.iloc[first_score_idx]
first_score_team = team_id_from_name(first_score_player)

first_shot = df_pos_dist_trunc[(df_pos_dist_trunc.closest_to_ball==first_score_player)&(df_pos_dist_trunc.period.period==1)&
(df_pos_dist_trunc.game_clock.game_clock>=697)&
(df_pos_dist_trunc.game_clock.game_clock<=701)]
first_shot_region = first_shot[first_score_player].x_loc.iloc[0]
if first_shot_region >= 50:
    
    
    
df = pd.DataFrame(np.random.random((4,4)))
df.columns = pd.MultiIndex.from_product([[1,2],['A','B']])
print df
added_col = [ [0,1,2, 3],
            [4, 5, 6, 7]]
 
orig_cols = list(df.columns.levels[0])
for i in range(len(orig_cols)):
    df[orig_cols[i],'dist']=added_col[i]

df = df.sort_index(axis=1)       
