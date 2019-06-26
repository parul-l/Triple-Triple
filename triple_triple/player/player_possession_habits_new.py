# delete triple_triple/player_possession_habits.py
import logging
import os
from triple_triple.data_generators.get_data import athena_to_pandas, list_for_sql

from triple_triple.config import SQL_DIR

# initiate logger
logger = logging.getLogger()
logger.setLevel('INFO')


def get_possession_table(
        players: list = [],
        gameids: list = [],
        date_range: list = ['1970-01-01', '2099-06-25'],
        distance_to_ball: int = 4, # square distance
        possession_block: int = 25 # min consecutive blocks to consider a possession
):

    gameids = get_gameid_given_player(players, date_range)

    # get gameids from playerlist
    if players:
        rel_games = get_gameid_given_player(players=players, date_range=date_range)
    elif gameids:
        rel_games = str(gameids)
    else:
        logger.error('Need to specify list of players or gameids')

    sql_path = os.path.join(SQL_DIR, 'player_possession_given_games.sql')

    # get query
    with open(sql_path) as f:
        query = f.read().format(
            list_for_sql(rel_games),
            distance_to_ball,
            possession_block
        )

    # figure out what I'd want to do with the query
    # execute it?
    # join with actions?
