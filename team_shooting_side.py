
def open_json(file_name):
    json_data = open(file_name).read()
    return json.loads(json_data)

def team_id_from_name(name):
    for value in game_id_dict.values():
        if value[0]==name:
            return value[2]      

# determine home_team and away_team
def teams_playing_from_raw(game_id, raw_data):
    hometeam_id = raw_data['events'][0]['home']['teamid']
    awayteam_id = raw_data['events'][0]['visitor']['teamid']    
    return hometeam_id, awayteam_id

# find index of first score
def first_team_shooting_side(df_play_by_play, df_positions, hometeam_id, awayteam_id):
    df_pos_dist = pos_and_dist(dataframe=df_positions)
    df_pos_dist_trunc = df_pos_dist[df_pos_dist.min_dist <=2]
    df_pos_dist_trunc = df_pos_dist_trunc.reset_index()
    
    # determine first score
    score = list(df_play_by_play.SCORE.values)
    first_score_idx = next(score.index(item) for item in score if type(item)==list)

    # find time, player 
    first_score_period = df_play_by_play.PERIOD.iloc[first_score_idx]
    first_score_game_clock = df_play_by_play.PCTIMESTRING.iloc[first_score_idx]
    first_score_player = df_play_by_play.PLAYER1_NAME.iloc[first_score_idx]
    first_score_team = team_id_from_name(first_score_player)

    # assuming it takes 4 seconds for ball to reach rim
    first_score = df_pos_dist_trunc[(df_pos_dist_trunc.closest_to_ball==first_score_player)&
                  (df_pos_dist_trunc.period.period==first_score_period)&
                  (df_pos_dist_trunc.game_clock.game_clock>=first_score_game_clock)&
                  (df_pos_dist_trunc.game_clock.game_clock<=first_score_game_clock+4)]

    first_score_xcoord = first_score[first_score_player].x_loc.iloc[0]
    if  (first_score_xcoord <= 47 and        
        first_score_team==hometeam_id) or (first_score_xcoord>47 and first_score_team==awayteam_id):        
        return {hometeam_id: 'left', awayteam_id: 'right'}
    elif (first_score_xcoord <= 47 and  
        first_score_team==awayteam_id) or (first_score_xcoord>47 and first_score_team==hometeam_id):        
        return {awayteam_id: 'left', hometeam_id: 'right'}
        
def team_shooting_side(player, period, shooting_side, hometeam_id, awayteam_id):
    team = team_id_from_name(player)
    if team==hometeam_id:
        if (period==1 or period==2):
            return shooting_side[team]
        elif (period==3 or period==4):
            return shooting_side[awayteam_id]
    elif team==awayteam_id:
        if (period==1 or period==2):
            return shooting_side[team]
        elif (period==3 or period==4):
            return shooting_side[hometeam_id]

##############################
##############################

if __name__=='__main__':
    import nbastats_game_data
    # should inmport open_json or just write the def as above
    from player_passing_habits import pos_and_dist
    from player_position_data import open_json
    
    # get the files needed
    df_play_by_play = play_by_play_df(base_url_play, params_play, HEADERS)
    game_id_dict = json.load(open('game_id_dict.json'))        
    # January 11, 2016: MIA @ GSW
    game_id = '0021500568'
    tracking_file = '/Users/pl/Downloads/' + game_id + '.json'
    raw_data = open_json(tracking_file)
    
    hometeam_id, awayteam_id = teams_playing_from_raw(game_id, raw_data)  
                
    shooting_side = first_team_shooting_side(df_play_by_play, df_positions, hometeam_id, awayteam_id)

    team_shooting_side(player, period, shooting_side, hometeam_id, awayteam_id)  
    
