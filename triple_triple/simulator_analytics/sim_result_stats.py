import numpy as np
import sklearn.metrics as metrics

from triple_triple.startup_data import (
    get_df_box_score_player_tracking,
    get_df_box_score_traditional
)


df_box_score_player_tracking = get_df_box_score_player_tracking()
df_box_score_traditional = get_df_box_score_traditional()


# Assuming players of interest played the whole game, we scale their parameters
def get_scaled_players_stats(df_actual_row):
    return 2880.0 / df_actual_row['MIN'] * df_actual_row[4:]


def get_result_stats(
    df_results_team0,
    df_results_team1,
    df_box_score_player_tracking,
    df_box_score_traditional,
    teams_list,
    hometeam_id=1610612744,
    awayteam_id=1610612748
):

    team0_players = teams_list[0].keys()
    team1_players = teams_list[1].keys()

    col_sim = [
        'PTS', 'FGA', 'FGM', 'FG3A', 'FG3M',
        'OREB', 'DREB', 'STL', 'BLK', 'TO', 'PASS'
    ]

    col_traditional = \
        ['PLAYER_NAME', 'PLAYER_ID', 'MIN', 'TEAM_ID'] + col_sim[:-1]

    # add passes to df_box_score_traditional and get relevant players
    rel_players = 'PLAYER_ID in @team0_players or PLAYER_ID in @team1_players'
    df_actual = df_box_score_traditional\
        .query(rel_players)[col_traditional]
    df_actual['PASS'] = df_box_score_player_tracking\
        .query(rel_players)['PASS']

    team0_sim_avg = df_results_team0[col_sim].mean().values
    team1_sim_avg = df_results_team1[col_sim].mean().values

    team0_sim_std = df_results_team0[col_sim].std().values
    team1_sim_std = df_results_team1[col_sim].std().values

    # get scaled player stats as if they played 48 min
    # originally had MIN > 0 but players are from teams_list which only include players that play
    team0_actual = df_actual\
        .query('TEAM_ID==@hometeam_id')\
        .apply(get_scaled_players_stats, axis=1)\
        .sum().values
    team1_actual = df_actual\
        .query('TEAM_ID==@awayteam_id')\
        .apply(get_scaled_players_stats, axis=1)\
        .sum().values

    return (
        team0_actual,
        team1_actual,
        team0_sim_avg,
        team1_sim_avg,
        team0_sim_std,
        team1_sim_std
    )


def get_root_mean_sq(df_results, team_actual):
    cols = list(df_results)
    cols.remove('NUM_PLAYS')

    error_array = np.zeros(len(cols))
    num_sim = len(df_results)
    for i in range(len(cols)):
        error = metrics.mean_squared_error(
            df_results[cols[i]].values,
            np.repeat(team_actual[i], num_sim)
        )
        error_array[i] = error

    return np.sqrt(error_array)


def get_r2(df_results, team_actual):
    cols = list(df_results)
    cols.remove('num_plays')

    r2_array = np.zeros(len(cols))
    num_sim = len(df_results)
    for i in range(len(cols)):
        r2 = metrics.r2_score(
            df_results[cols[i]].values,
            np.repeat(team_actual[i], num_sim)
        )

        r2_array[i] = r2

    return r2_array
