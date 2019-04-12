import psycopg2
import pandas.io.sql as psql

POSTGRES_CONNECTION_PARAMS = {
    'dbname': 'pl',
    'host': 'localhost',
    'user': 'pl'
}


def get_dataframe(
            query,
            game_id,
            connection_params=POSTGRES_CONNECTION_PARAMS
    ):
    connection = psycopg2.connect(**connection_params)
    return psql.read_sql(query.format(game_id), connection)


def get_game_specific_tables(game_id):
    games_query = """
        SELECT * 
          FROM games
        WHERE id ='{}';
    """
    play_by_play_query = """
        SELECT *, 
          score_home - score_visitor AS score_diff
          FROM play_by_play
        WHERE game_id ='{}'
        ORDER BY event_id ASC;
    """
    game_positions_query = """
        SELECT *
          FROM game_positions
        WHERE game_id ='{}'
        ORDER BY time_stamp;
    """

    return {
        'df_games': get_dataframe(games_query, game_id),
        'df_play_by_play': get_dataframe(play_by_play_query, game_id),
        'df_game_positions': get_dataframe(game_positions_query, game_id),
    }
