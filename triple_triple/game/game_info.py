import pandas as pd


from triple_triple.connection import get_connection
from triple_triple.data_generators.get_data import (
    athena_to_pandas,
    execute_athena_query,
    get_query_response,
    list_for_sql
)


def get_gameid_given_dates(date_range: list = ['1970-01-01', '2019-06-25']):
    """
        This function takes a date range and returns a tuple all gameids
        that fall in this range 
    
    Parameters
    ----------
        data_range: `list`
            A list of length two given the start and 
            end dates (inclusive) of the time period of interest.
            Date is in the form 'YYYY-MM-DD'.
    
    Returns
    -------
    A `list` of unique gameids of all games within the specified date range 
    """

    query = """
        SELECT DISTINCT 
          gameid
        FROM nba.gameinfo
        WHERE gamedate BETWEEN '{}' AND '{}'
    """.format(date_range[0], date_range[1])

    df = athena_to_pandas(
        query=query,
        output_filename='gameids_{}_to_{}'.format(date_range[0], date_range[1])
    )
    # ensure gameids in correct format
    df.loc[:, 'gameid'] =  df.gameid.apply(lambda x: str(x).zfill(10))

    return list(df.gameid.values)


def get_date_given_gameid(gameid: str, max_time: int = 5):
    """
        This function takes a date range and returns a tuple all gameids
        that fall in this range 
    
        Parameters
        ----------
            gameids: `str`
                A gameids.
            max_time: `int`
        
        Returns
        -------
            A `str` of the game date of the given gameid
    """

    query = """
        SELECT 
          gamedate
        FROM nba.gameinfo
        WHERE gameid = '{}'
    """.format(gameid)

    execute_response = execute_athena_query(
        query=query,
        database='nba',
        output_filename='gamedate_{}'.format(gameid),
    )
    execution_id = execute_response['QueryExecutionId']
    query_results = get_query_response(
        execution_id=execution_id,
        max_time=max_time
    )
    try:
        return query_results['ResultSet']['Rows'][1]['Data'][0]['VarCharValue']
    except:
        logger.info('Date not computed')
        return None


def get_gameid_given_player(
    players: list,
    date_range: list = ['1970-01-01', '2099-06-25']
):
    """
        This function takes a list of playerids and returns a list all gameids
        those players have played in
    
        Parameters
        ----------
            players: `list`
                A list of the playerids of interest.

            data_range: `list`
                A list of length two given the start and 
                end dates (inclusive) of the time period of interest.
                Date is in the form 'YYYY-MM-DD'.
        
        Returns
        -------
        A `list` of unique gameids of all games the collective group of players
        have played in within the specified date range 
    """

    # gameids = list_for_sql(get_gameid_given_dates(date_range))
    playerids = list_for_sql(players)

    # query = """
    #     SELECT DISTINCT gameid
    #     FROM nba.playerinfo 
    #     WHERE gameid IN {}
    #     AND playerid IN {}
        
    # """.format(gameids, playerids)

    query = """
        WITH games AS (
            SELECT DISTINCT gameid
            FROM nba.gameinfo
            WHERE gamedate BETWEEN '{}' AND '{}'
        )
        SELECT DISTINCT games.gameid
        FROM nba.playerinfo 
        INNER JOIN games
          ON games.gameid = playerinfo.gameid
          AND playerid IN {}
    """.format(date_range[0], date_range[1], playerids)


    df = athena_to_pandas(
        query=query,
        output_filename='gameids_given_players'
    )
    # ensure gameids in correct format
    df.loc[:, 'gameid'] = df.gameid.apply(lambda x: str(x).zfill(10))

    return list(df.gameid.values)


