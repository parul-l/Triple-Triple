import pandas as pd
import requests


def get_data(base_url, params, headers):
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

# all_games_stats has stats for every game played in
# specified season for each team;
# ie. each game is listed twice
# determine which teams are playing based on game_id


def time_in_seconds(time):
    t = time.split(':')
    return int(t[0]) * 60 + int(t[1])


def score_in_int(score):
    try:
        return [int(score.split('-')[0]), int(score.split('-')[1])]
    except:
        return score


def teams_playing(game_id, all_games_stats):
    game_info = [
        item for item in all_games_stats['resultSets'][0]['rowSet'] if
        item[4] == game_id
    ]

    if game_info[0][6].split()[1] == 'vs.':
        home_team = game_info[0][1]
        away_team = game_info[1][1]
    elif game_info[0][6].split()[1] == '@':
        home_team = game_info[1][1]
        away_team = game_info[0][1]

    return str(home_team), str(away_team)


def play_by_play_df(base_url_play, params_play, headers):
    play_data = get_data(base_url_play, params_play, headers)

    headers_play_by_play = [
        "Game_ID",
        "PERIOD",
        "WCTIMESTRING",
        "PCTIMESTRING",
        "HOMEDESCRIPTION",
        "NEUTRAL DESCRIPTION",
        "VISITORDESCRIPTION",
        "SCORE",  # [Away, Home]
        "PLAYER1_ID",
        "PLAYER1_NAME",
        "PLAYER1_TEAM_ID",
        "PLAYER2_ID",
        "PLAYER2_NAME",
        "PLAYER2_TEAM_ID",
        "PLAYER3_ID",
        "PLAYER3_NAME",
        "PLAYER3_TEAM_ID"
    ]

    play_by_play = []
    len_plays = len(play_data['resultSets'][0]['rowSet'])

    for i in range(len_plays):
        each_play = play_data['resultSets'][0]['rowSet'][i]
        play_by_play.append([
            each_play[0],
            each_play[4],
            each_play[5],
            time_in_seconds(each_play[6]),
            each_play[7],
            each_play[8],
            each_play[9],
            score_in_int(each_play[10]),
            each_play[13],
            each_play[14],
            each_play[15],
            each_play[20],
            each_play[21],
            each_play[22],
            each_play[27],
            each_play[28],
            each_play[29]]
        )

    # create a data frame from the list
    return pd.DataFrame(play_by_play, columns=headers_play_by_play)


def box_score_df(base_url_box_score, params_box_score, headers):
    box_score_data = get_data(base_url_box_score, params_box_score, headers)
    df_box_score = pd.DataFrame(
        box_score_data['resultSets'][0]['rowSet'] +
        box_score_data['resultSets'][0]['rowSet'],
        columns=box_score_data['resultSets'][0]['headers']
    ).drop_duplicates()
    df_box_score['MIN'] = pd.to_datetime(df_box_score['MIN'], format='%M:%S')
    return df_box_score
