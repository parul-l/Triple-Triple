import logging
import os

from triple_triple.data_generators.get_data import (
    check_view_exists,
    execute_athena_query,
    list_for_sql
)
from triple_triple.game.game_info import (
    get_gameid_given_player
)
from triple_triple.config import SQL_DIR

# initiate logger
logger = logging.getLogger()
logger.setLevel('INFO')


def create_court_region_view(gameids: list, playerids: list):
    """
        Takes a list of playerids and gameids and creates a view
        to show the player's court region for every (x, y) coordinate pair

        Params:
            gameids: `list` The gameids of interest for the court-region view

            playerids: `list` The playerids from the gameids specified above, for 
            which the court regions are to be found.       

    """

    # court region query
    court_region_sql_path = os.path.join(
        SQL_DIR,
        'court',
        'court_region_query_view.sql'
    )
    with open(court_region_sql_path) as f:
        court_query = f.read().format(
            list_for_sql(gameids),
            list_for_sql(gameids),
            list_for_sql(playerids)
        )

    # drop views if this exist
    logger.info('Dropping court-region view for given players')
    response_drop_court = execute_athena_query(
        query='DROP VIEW IF EXISTS nba.vw_courtregion;',
        database='nba',
        output_filename='drop_courtregion_vw',
    )

    try:
        # create courtregion view
        logger.info('Creating court-region view for given players')
        response_court = execute_athena_query(
            query=court_query,
            database='nba',
            output_filename='create_courtregion_vw',
        )
        return response_court

    except Exception as err:
        logger.error(err)


def create_possession_view(
        playerids: list,
        gameids: list = [],
        date_range: list = ['1970-01-01', '2099-06-25'],
        distance_to_ball: int = 4, # square distance
        possession_block: int = 7.5, # min consecutive blocks to consider a possession (0.8th of a second)
):
    """
        Takes a list of players and date range, and gets the possession
        table of all games the player has played in. Can also specify gameids
        if we know the games

        Default possession block is set to 7.5. There are 25 frames per second
        and the NBA considers 0.3s as the min time for a catch and shoot.
        Hence I chose 25 * 0.3 = 7.5 as number of consecutive blocks to be considered
        a possession.
    """

    # get gameids from playerlist
    player_gameids = get_gameid_given_player(
        players=playerids,
        date_range=date_range
    )

    if gameids:
        gameids = list(set(player_gameids) & set(gameids))
    else:
        gameids = player_gameids
        
    # create court_region view
    response_court = create_court_region_view(gameids=gameids, playerids=playerids)

    if check_view_exists(
        database='nba',
        view_name='vw_courtregion',
        max_time=180
    ):
        # get possession query
        possession_sql_path = os.path.join(
            SQL_DIR, 
            'players',
            'player_possession_given_games_view.sql'
        )

        with open(possession_sql_path) as f:
            poss_query = f.read().format(
                list_for_sql(gameids),  # gameid
                distance_to_ball,
                possession_block
            )

        # drop view if it exists
        logger.info('Dropping possession-region view for given players')
        response_poss = execute_athena_query(
            query='DROP VIEW IF EXISTS nba.vw_possession;',
            database='nba',
            output_filename='drop_poss_tmp_vw',
        )

        # create possession view
        logger.info('Creating possession-region view for given players')
        response_poss = execute_athena_query(
            query=poss_query,
            database='nba',
            output_filename='create_poss_tmp_vw',
        )

        return response_poss
    

def create_action_region_view(
        playerids: list,
        gameids: list = [],
        date_range: list = ['1970-01-01', '2099-06-25'],
        distance_to_ball: int = 4,  # square distance
        possession_block: int = 7.5 # min consecutive blocks to consider a possession (0.8th of a second)
):

    response_poss = create_possession_view(
        playerids=playerids,
        gameids=gameids,
        date_range=date_range,
        distance_to_ball=distance_to_ball, 
        possession_block=possession_block 
    )

    # allow 10 seconds for view to be created
    if check_view_exists(
        database='nba',
        view_name='vw_possession',
        max_time=180
    ):
        # action region query
        action_region_sql_path = os.path.join(
            SQL_DIR,
            'players',
            'action_region_view.sql'
        )
        with open(action_region_sql_path) as f:
            action_region_query = f.read().format(
                list_for_sql(gameids),
                list_for_sql(playerids)
            )

        # drop view if it exists
        logger.info('Dropping action-region view for given players')
        response_poss = execute_athena_query(
            query='DROP VIEW IF EXISTS nba.vw_action_region;',
            database='nba',
            output_filename='drop_action_region_vw',
        )
        # create actionregion view
        logger.info('Creating action-region view for given players')
        response_action_region = execute_athena_query(
            query=action_region_query,
            database='nba',
            output_filename='create_actionregion_vw',
        )

        vw_action_exists = check_view_exists(
            database='nba',
            view_name='vw_action_region',
            max_time=180
        )

        return response_action_region

    return response_poss

