import pandas as pd


def playerid_from_name(player_name, game_id_dict):
    for playerid, player_info in game_id_dict.items():
        if player_info[0] == player_name:
            return playerid


def player_team_loc_from_name(player_name, game_id_dict, hometeam_id):
    player_id = playerid_from_name(player_name, game_id_dict)
    team_id = game_id_dict[player_id][2]
    if team_id == hometeam_id:
        return team_id, 'home'
    else:
        return team_id, 'away'


def player_impact_df(player_name, team_info_list, game_id_dict, df_play_by_play):
    if team_info_list[1] == 'home':
        descrip = 'HOMEDESCRIPTION'
    elif team_info_list[1] == 'away':
        descrip = 'VISITORDESCRIPTION'

    playerid = int(playerid_from_name(player_name, game_id_dict))

    df_pbp_player = df_play_by_play[
        (df_play_by_play['PLAYER1_ID'] == playerid) |
        (df_play_by_play['PLAYER2_ID'] == playerid) |
        (df_play_by_play['PLAYER3_ID'] == playerid)
    ]

    # drop NaN descriptions (= player is fouled)
    df_pbp_player = df_pbp_player[pd.notnull(df_pbp_player[descrip])]
    df_pbp_player = df_pbp_player.reset_index()
    df_player_impact = df_pbp_player[['PERIOD', 'PCTIMESTRING', descrip]]

    return df_player_impact


def player_game_stats_nba(player_name, game_id_dict, df_player_impact):
    playerid = playerid_from_name(player_name, game_id_dict)
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
        descrip_split = df_player_impact.ix[:, 2].iloc[i].split()
        if (descrip_split[-3] == '(' + player_lastname and
                descrip_split[-1] == 'AST)'):
            assist.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif 'Turnover' in df_player_impact.ix[:, 2].iloc[i]:
            turnover.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif (descrip_split[0] == player_lastname and
              descrip_split[1] == 'Free' and
              descrip_split[2] == 'Throw'):
            free_throw.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif (descrip_split[0] == player_lastname and
              descrip_split[1] == 'REBOUND'):
            rebound.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif (descrip_split[0] == player_lastname and
              descrip_split[1] == 'STEAL'):
            steal.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif (descrip_split[0] == player_lastname and
              descrip_split[1] == 'BLOCK'):
            block.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif (descrip_split[0] == player_lastname and
              'FOUL' in descrip_split[1]):
            commit_foul.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])

        elif ((descrip_split[0] == 'MISS' and 'Free Throw' not in
              df_player_impact.ix[:, 2].iloc[i]) or
              (descrip_split[0] == player_lastname and
               'PTS' in df_player_impact.ix[:, 2].iloc[i] and
               'Free Throw' not in df_player_impact.ix[:, 2].iloc[i])):
            shoot.append([
                df_player_impact.iloc[i]['PERIOD'],
                df_player_impact.iloc[i]['PCTIMESTRING'],
                df_player_impact.ix[:, 2].iloc[i]
            ])
    return [
        assist,
        block,
        commit_foul,
        free_throw,
        rebound,
        shoot,
        steal,
        turnover
    ]
