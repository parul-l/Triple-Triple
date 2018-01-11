import unittest
import mock

from triple_triple.import_postgres_tables import (
    POSTGRES_CONNECTION_PARAMS,
    get_dataframe,
    get_game_specific_tables
)


class TestImportPostgresTables(unittest.TestCase):
    """Tests for import_postgres_tables.py"""
    
    def test_get_dataframe(self, connection_params=POSTGRES_CONNECTION_PARAMS):
        psycopg2_mock = mock.Mock()
        psql_mock = mock.Mock()

        patches = {
            'psycopg2': psycopg2_mock,
            'psql': psql_mock
        }
        
        path = 'triple_triple.import_postgres_tables'
        with mock.patch.multiple(path, **patches):
            get_dataframe(
                query='test query {}',
                game_id='1234'
            )

        psycopg2_mock.connect.assert_called_once_with(**connection_params)    
        psql_mock.read_sql.assert_called_once_with(
            'test query 1234',
            psycopg2_mock.connect(**connection_params)
        )

    def test_get_game_specific_tables(self):
        get_dataframe_mock = mock.Mock()
        
        queries = [
            'games_mock',
            'play_by_play_mock',
            'game_positions_mock'
        ]

        path = 'triple_triple.import_postgres_tables.get_dataframe'
        with mock.patch(path, get_dataframe_mock):
            get_game_specific_tables('1234')

        get_dataframe_mock.has_calls_with(
            [mock.call(f, '1234') for f in queries]
        )


if __name__ == '__main__':
    unittest.main()
