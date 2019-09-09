import logging
import os

import pandas as pd
import numpy as np

from triple_triple.game.game_info import get_gameid_given_dates
from triple_triple.data_generators.get_data import (
    athena_to_pandas,
    get_query_results
)
from triple_triple.player.player_possession_habits_new import (
    get_player_action_frequency
)


# initiate logger
logger = logging.getLogger()
logger.setLevel('INFO')
logging.getLogger().addHandler(logging.StreamHandler())


def add_data_for_gameids(

):


def player_action_frequency_query(
    date_range: list,  # [start_date, end_date]
    playerid: int, 
):

    return """
        SELECT 
              region_code
            , court_region
            , CASE 
                WHEN event_action IN ('field goal made', 'field goal missed') THEN 'field_goal'
                ELSE event_action
              END AS event_action
            , action_region_frequency
        FROM nba.player_action_frequency
        WHERE playerid = '{}'
            AND gamedate between '{}' AND '{}'
    """.format(playerid, date_range[0], date_range[1])
    

def player_action_frequency_per_game(
        playerid: int,
        date_range: list = [], # [start_date, end_date]
        gameids: list = [],
        max_time: int = 10
):
    """
        This function determines the action frequency per region for a given player.    
        The function requires either (i) a date range or (ii) list of gameids,
        to obtain player frequency data from either (i) or (ii) or the 
        intersection of both
    """
    if not date_range and not gameids:
        logger.error('Need to specify date_range OR gameids OR both.')

    if date_range:
        gameid_dates = get_gameid_given_dates(date_range)
        if gameids:
            gameids = list(set(gameid_dates) & set(gameids))
        else:
            gameids = gameid_dates
    
    # find all games whose player frequency is not yet computed
    query = """
        SELECT DISTINCT 
            gameid
        FROM nba.player_action_frequency
        WHERE playerid = '{}'
    """.format(playerid)

    query_results = get_query_results(
        query=query,
        output_filename='gameids_for_player_{}'.format(playerid),
        max_time=max_time,
    )
    gameids_present = [
        data['Data'][0]['VarCharValue']
        for data in query_results['ResultSet']['Rows']
    ] # includes header
    gameids_toadd = list(set(gameids) - set(gameids_present[1:]))

    # if non-empty, add the frequency data for missing games
    if gameids_toadd:
        # get_player_action_frequency already runs the etl
        etl = get_player_action_frequency(
            playerids=[playerid],
            gameids=gameids_toadd,
            date_range=date_range
        )

    # get dataframe of frequencies
    output_query = player_action_frequency_query(
        date_range=date_range, 
        playerid=playerid
    )

    return athena_to_pandas(
        query=output_query,
        output_filename='player_action_frequency'
    )


def get_player_probability(player_action_frequency: pd.DataFrame):
    df_pivot = pd.pivot_table(
        player_action_frequency,
        index=['region_code', 'court_region'],
        values='action_region_frequency',
        columns='event_action',
        aggfunc=np.max,
        fill_value=0
    )

    # output example
    # event_action                assist  field_goal   rebound  steal  turnover
    # region_code court_region
    # 0           paint         0.000000    0.500000  0.500000  0.000  0.000000
    # 2           midrange      0.333333    0.333333  0.000000  0.000  0.333333
    # 3           perimeter     0.111111    0.666667  0.111111  0.000  0.111111
    # 4           backcourt     0.125000    0.000000  0.625000  0.125  0.125000

    return df_pivot.div(df_pivot.sum(axis=1), axis=0)


def player_position_probability(
        playerid: int,
        date_range: list = [],  # [start_date, end_date]
        gameids: list = [],
        max_time: int = 10
):
    if not date_range and not gameids:
        logger.error('Need to specify date_range OR gameids OR both.')

    if date_range:
        gameid_dates = get_gameid_given_dates(date_range)
        if gameids:
            gameids = list(set(gameid_dates) & set(gameids))
        else:
            gameids = gameid_dates

    query = """
        SELECT
            region_code
            , vw_courtregion.court_region
            , COUNT(vw_courtregion.court_region)            AS region_frequency
            , COUNT(vw_courtregion.court_region) * 1.0 / (SELECT COUNT(*) FROM nba.vw_courtregion WHERE playerid = {0}) 
                                                            AS region_probability
        FROM nba.vw_courtregion
          LEFT JOIN nba.court_region_codes
          ON vw_courtregion.court_region = court_region_codes.court_region
        WHERE playerid = {0}
        GROUP BY region_code, vw_courtregion.court_region
    """.format(playerid)


    results = get_query_results(
        query=query,
        output_filename='player_position_prob',
        max_time=max_time
    )
    data = [
        [subrow['VarCharValue'] for subrow in row['Data']]
        for row in results['ResultSet']['Rows']
    ]
    return pd.DataFrame(data=data[1:], columns=data[0])


def player_possession_probability(
        playerid: int,
        date_range: list = [],  # [start_date, end_date]
        gameids: list = [],
        max_time: int = 10
):
    if not date_range and not gameids:
        logger.error('Need to specify date_range OR gameids OR both.')

    if date_range:
        gameid_dates = get_gameid_given_dates(date_range)
        if gameids:
            gameids = list(set(gameid_dates) & set(gameids))
        else:
            gameids = gameid_dates

    query = """
        WITH player_poss AS (
            SELECT
                  gameid
                , COUNT(DISTINCT enumerated_blocks)		AS num_possession
            FROM nba.vw_possession
            WHERE 
                has_ball = 1 AND 
                vw_possession.playerid = {} AND
                vw_possession.gameids IN {}
            GROUP BY vw_possession.gameid
        )
        , all_poss AS (
            SELECT
                gameid
                , COUNT(DISTINCT enumerated_blocks) AS total_possessions
            FROM nba.vw_possession 
            WHERE has_ball = 1
            GROUP BY gameid 
        )
        SELECT
              player_poss.gameid
            , num_possession
            , total_possessions
            , num_possession / total_possessions * 1.0      AS prob_possession
        FROM player_poss
        LEFT JOIN all_poss
        ON player_poss.gameid = all_poss.gameid
    """.format(playerid)

    results = get_query_results(
        query=query,
        output_filename='player_possession_prob',
        max_time=max_time
    )
