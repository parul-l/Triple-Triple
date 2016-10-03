import pandas as pd

from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_pos_dist,
    get_df_play_by_play,
)

game_id_dict = get_game_id_dict()
df_pos_dist = get_df_pos_dist()
df_play_by_play = get_df_play_by_play()

def playerid_from_name(player, player_info_dict=game_id_dict):
    for key, value in game_id_dict.items():
        if value[0]==player:
            return key


def player_impact_df(player_name, hometeam_id, dataframe=df_play_by_play):
    playerid = int(playerid_from_name(player_name))
    df_pbp_player = dataframe[
                    (dataframe['PLAYER1_ID']==playerid)|
                    (dataframe['PLAYER2_ID']==playerid)|       
                    (dataframe['PLAYER3_ID']==playerid)
    ]

    if df_pbp_player.iloc[0]['PLAYER1_ID']==playerid:
        if df_pbp_player.iloc[0]['PLAYER1_TEAM_ID']==hometeam_id:
            descrip='HOMEDESCRIPTION'
        else:
            descrip='VISITORDESCRIPTION'

    elif df_pbp_player.iloc[0]['PLAYER2_ID']==playerid:
        if df_pbp_player.iloc[0]['PLAYER2_TEAM_ID']==hometeam_id:
            descrip='HOMEDESCRIPTION'
        else:
            descrip='VISITORDESCRIPTION'
    elif df_pbp_player.iloc[0]['PLAYER3_ID']==playerid:
        if df_pbp_player.iloc[0]['PLAYER3_TEAM_ID']==hometeam_id:
            descrip='HOMEDESCRIPTION'
        else:
            descrip='VISITORDESCRIPTION'

    # drop NaN descriptions (=player is fouled)
    df_pbp_player = df_pbp_player[pd.notnull(df_pbp_player[descrip])]
    df_pbp_player = df_pbp_player.reset_index()
    df_player_impact = df_pbp_player[['PERIOD', 'PCTIMESTRING',
    descrip]]

    return df_player_impact


def player_game_stats_nba(player_name, df_player_impact):
    playerid = playerid_from_name(player_name)
    player_lastname = game_id_dict[playerid][0].split()[1]

    assist = []
    block = []
    commit_foul = []
    free_throw = []
    rebound = []
    shoot = []
    steal = []
    turnover = []

    for i in range(len(df_player_impact)):
        descrip_split = df_player_impact.ix[:,2].iloc[i].split()
        if (descrip_split[-3]=='('+ player_lastname and
            descrip_split[-1]=='AST)'):
            assist.append([df_player_impact.iloc[i]['PERIOD'],
                           df_player_impact.iloc[i]['PCTIMESTRING'],
                           df_player_impact.ix[:,2].iloc[i]])

        elif 'Turnover' in df_player_impact.ix[:,2].iloc[i]:
            turnover.append([df_player_impact.iloc[i]['PERIOD'],
                           df_player_impact.iloc[i]['PCTIMESTRING'],
                           df_player_impact.ix[:,2].iloc[i]])

        elif (descrip_split[0]==player_lastname and
              descrip_split[1]=='Free' and
              descrip_split[2]=='Throw'):
            free_throw.append([df_player_impact.iloc[i]['PERIOD'],
                             df_player_impact.iloc[i]['PCTIMESTRING'],
                             df_player_impact.ix[:,2].iloc[i]])

        elif (descrip_split[0]==player_lastname and
              descrip_split[1]=='REBOUND'):
            rebound.append([df_player_impact.iloc[i]['PERIOD'],
                            df_player_impact.iloc[i]['PCTIMESTRING'],
                            df_player_impact.ix[:,2].iloc[i]])
        elif (descrip_split[0]==player_lastname and
              descrip_split[1]=='STEAL'):
            steal.append([df_player_impact.iloc[i]['PERIOD'],
                            df_player_impact.iloc[i]['PCTIMESTRING'],
                            df_player_impact.ix[:,2].iloc[i]])
        elif (descrip_split[0]==player_lastname and
              descrip_split[1]=='BLOCK'):
            block.append([df_player_impact.iloc[i]['PERIOD'],
                            df_player_impact.iloc[i]['PCTIMESTRING'],
                            df_player_impact.ix[:,2].iloc[i]])
        elif (descrip_split[0]==player_lastname and
              'FOUL' in descrip_split[1]):
            commit_foul.append([df_player_impact.iloc[i]['PERIOD'],
                            df_player_impact.iloc[i]['PCTIMESTRING'],
                            df_player_impact.ix[:,2].iloc[i]])
        elif ((descrip_split[0]=='MISS' and 'Free Throw' not in
              df_player_impact.ix[:,2].iloc[i] )
              or
             (descrip_split[0]==player_lastname and
              'PTS' in df_player_impact.ix[:,2].iloc[i] and
              'Free Throw' not in df_player_impact.ix[:,2].iloc[i])):
            shoot.append([df_player_impact.iloc[i]['PERIOD'],
                            df_player_impact.iloc[i]['PCTIMESTRING'],
                            df_player_impact.ix[:,2].iloc[i]])
    return [assist, block, commit_foul, free_throw, rebound, shoot, steal, turnover]

###########################
###########################

if __name__=='__main__':
    player = 'Chris Bosh'

    df_player_impact = player_impact_df(player, hometeam_id)
    player_game_stats = player_game_stats_nba(player, df_player_impact)
