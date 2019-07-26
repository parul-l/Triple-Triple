# delete triple_triple/player_possession_habits.py
import logging
import os
from triple_triple.data_generators.get_data import (
    athena_to_pandas,
    execute_athena_query,
    list_for_sql
)
from triple_triple.game.game_info import (
    get_gameid_given_dates,
    get_gameid_given_player
)
from triple_triple.config import SQL_DIR

# initiate logger
logger = logging.getLogger()
logger.setLevel('INFO')


def create_possession_view(
        players: list,
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
    player_gameids = get_gameid_given_player(players=players, date_range=date_range)

    if gameids:
        gameids = list(set(player_gameids) & set(gameids))
    else:
        gameids = player_gameids
        
    # court region query
    court_region_sql_path = os.path.join(
        SQL_DIR,
        'court',
        'court_region_query_view.sql'
    )
    with open(court_region_sql_path) as f:
        court_query = f.read().format(
            'nba.vw_courtregion', # view name
            list_for_sql(gameids),
            list_for_sql(gameids),
            list_for_sql(players)
        )

    # get possession query
    possession_sql_path = os.path.join(
        SQL_DIR, 
        'players',
        'player_possession_given_games.sql'
    )

    with open(possession_sql_path) as f:
        poss_query = f.read().format(
            list_for_sql(gameids),  # gameid
            distance_to_ball,
            possession_block
        )

    # create courtregion view
    response_court = execute_athena_query(
        query=court_query,
        database='nba',
        output_filename='create_courtregion_vw', 
    )
    # create possession view
    response_poss = execute_athena_query(
        query=poss_query,
        database='nba',
        output_filename='create_poss_tmp_vw',
    )


def create_characterize_possession(
        players: list,
        gameids: list = [],
        date_range: list = ['1970-01-01', '2099-06-25'],
        distance_to_ball: int = 4,  # square distance
        possession_block: int = 7.5, # min consecutive blocks to consider a possession (0.8th of a second)
        drop_court_vw: bool = 0,
        drop_poss_vw: bool = 0
):

    create_possession_view(
        players=players,
        gameids=gameids,
        date_range=date_range,
        distance_to_ball=distance_to_ball, 
        possession_block=possession_block 
    )

    # action region query
    action_region_sql_path = os.path.join(
        SQL_DIR,
        'players',
        'characterize_player_possession.sql'
    )
    with open(action_region_sql_path) as f:
        action_region_query = f.read().format(
            'nba.vw_action_region',  # view name
            list_for_sql(gameids),
            list_for_sql(players)
        )

    # drop views
    if drop_court_vw:
        response_poss = execute_athena_query(
            query='DROP VIEW IF EXISTS nba.vw_poss_tmp;',
            database='nba',
            output_filename='drop_poss_tmp_vw',
        )
    if drop_poss_vw:
        response_drop_court = execute_athena_query(
            query='DROP VIEW IF EXISTS nba.vw_courtregion;',
            database='nba',
            output_filename='drop_courtregion_vw',
        )
