import unittest

import mock
import numpy as np
import pandas as pd

import triple_triple.plot.play_animation as pa


class TestPlayAnimation(unittest.TestCase):
    """Tests for play_animation.py"""

    def test_get_fixedtime(self):
        headers = ['game_clock', 'period', 'team_id']
        game_clock = np.tile(np.arange(14, -1, -1), 2)
        # shot_clock = np.arange(10, 7.5, -0.25).repeat(3)
        period = np.array([1, 2]).repeat(15)
        team_ids = np.tile([100, 100, 100, 100, 222, 222], 5)

        mock_df = pd.DataFrame(
            data=np.array([game_clock, period, team_ids]).T,
            columns=headers
        )

        df = pa.get_fixedtime_df(
            period=1,
            time_start=11,
            time_end=9,
            dataframe=mock_df
        )
        self.assertEqual(df.shape[0], 3)
        self.assertEqual(df.team_id.values.tolist(), [100, 222, 222])

        np.testing.assert_array_equal(df.period.values, 1)
        np.testing.assert_array_equal(9 <= df.game_clock.values, True)
        np.testing.assert_array_equal(df.game_clock.values <= 11, True)


if __name__ == '__main__':
    unittest.main()
