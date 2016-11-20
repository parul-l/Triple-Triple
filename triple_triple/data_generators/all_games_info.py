import pandas as pd


def all_games_info_df(all_games_stats_data):
    game_data = []
    game_info = all_games_stats_data['resultSets'][0]['rowSet']
    no_games = len(game_info)
    for i in range(no_games):
        game_data.append([
            str(game_info[i][4]),    # game_id
            game_info[i][5],         # date,
            str(game_info[i][1]),    # team id
            game_info[i][2],         # team abbrev
            game_info[i][6]          # match-up
        ])
    headers = ['game_id', 'game_date', 'team_id', 'team', 'match_up']
    df_game_info_raw = pd.DataFrame(game_data, columns=headers)
    # sort the games by id
    df_game_info_raw = df_game_info_raw.sort_values('game_id')\
        .reset_index(drop=True)

    # remove the duplicate games
    df_game_info = df_game_info_raw[::2].reset_index(drop=True)
    # use df_game_info_raw to get team_ids for both home and away team

    hometeam_id = []
    hometeam_abbrev = []
    awayteam_id = []
    awayteam_abbrev = []

    for idx in range(0, len(df_game_info)):
        match_up = df_game_info.match_up.iloc[idx].split()
        if match_up[1] == 'vs.':
            hometeam_id.append(df_game_info.team_id.iloc[idx])
            hometeam_abbrev.append(match_up[0])
            awayteam_id.append(df_game_info_raw.team_id.iloc[2 * idx + 1])
            awayteam_abbrev.append(match_up[2])
        elif match_up[1] == '@':
            awayteam_id.append(df_game_info.team_id.iloc[idx])
            awayteam_abbrev.append(match_up[0])
            hometeam_id.append(df_game_info_raw.team_id.iloc[2 * idx + 1])
            hometeam_abbrev.append(match_up[2])

    df_game_info = df_game_info.drop(['team_id', 'team'], axis=1)

    game_info_sorted_dict = {
        'hometeam_id': hometeam_id,
        'hometeam_abbrev': hometeam_abbrev,
        'awayteam_id': awayteam_id,
        'awayteam_abbrev': awayteam_abbrev
    }
    df_game_info_sorted = pd.DataFrame(data=game_info_sorted_dict)

    return df_game_info.join(df_game_info_sorted)
