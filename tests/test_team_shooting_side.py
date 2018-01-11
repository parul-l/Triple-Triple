import datetime
import os
import pandas as pd
import unittest
import mock

from triple_triple.team_shooting_side import get_initial_shooting_sides
from triple_triple.config import MOCK_DATASETS_DIR

class TestTeamShootingSide(unittest.TestCase):
    """ Tests for team_shooting_side.py """
    
    def test_get_initial_shooting_sides(self):
        np_mock = mock.Mock()
        pd_mock = mock.Mock()

        df_play_by_play = pd.read_csv(
            os.path.join(MOCK_DATASETS_DIR, 'play_by_play_snippet.csv'),
            index_col=0
        )
        df_games = pd.read_csv(
            os.path.join(MOCK_DATASETS_DIR, 'games_snippet.csv'),
            index_col=0
        )
        df_game_positions = pd.read_csv(
            os.path.join(MOCK_DATASETS_DIR, 'game_positions_snippet.csv'),
            index_col=0
        )
        # Add row to df_game_positions
        # so that first_score_period, game_clock, team
        # are in df_game_positions_snippet
        x_coordinates = [10, 50]
        positions = [('left', 'right'), ('right', 'left')]
        
        for x_coord, pos in zip(x_coordinates, positions):
            new_row = [
                'newrow',
                100,
                datetime.datetime(2016, 1, 1, 19, 40, 50),
                1,
                695,        # using first_score_game_clock
                24,
                1610612761,
                -1,         # ball id
                x_coord,
                20,
                0
            ]
            df_game_positions = df_game_positions.append(pd.DataFrame(
                [new_row], columns=list(df_game_positions)),
            )
            ans = get_initial_shooting_sides(
                df_games=df_games,
                df_play_by_play=df_play_by_play,
                df_game_positions=df_game_positions
            )
            assert ans[1610612761] == pos[0]
            assert ans[1610612766] == pos[1]


if __name__ == '__main__':
    unittest.main()
