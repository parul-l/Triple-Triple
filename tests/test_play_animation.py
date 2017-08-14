import unittest

import numpy as np
import pandas as pd

import triple_triple.plot.play_animation as pa

# TODO: Test plot_points, annotate_points, update_annotations, play_animation


def rand_coord_generator(lower_bound, upper_bound, len_array):
    t = np.random.random(len_array)
    return (1 - t) * lower_bound + t * upper_bound


def make_mock_df():
    headers = [
        'game_clock',
        'shot_clock',
        'period',
        'team_id',
        'player_ids',
        'player_jersey',
        'x_loc',
        'y_loc'
    ]
    game_clock = np.array(np.arange(14, 8, -1)).repeat(5)
    shot_clock = np.array(np.arange(10, 4, -1)).repeat(5)
    period = np.array([1, 2, 3]).repeat(10)
    team_ids = np.tile([-1, 100, 100, 222, 222], 6)
    player_ids = np.tile(np.arange(-1, 4), 6)
    player_jersey = np.tile([-1, 51, 52, 53, 54], 6)
    x_loc = rand_coord_generator(lower_bound=47, upper_bound=94, len_array=30)
    y_loc = rand_coord_generator(lower_bound=0, upper_bound=50, len_array=30)

    mock_df = pd.DataFrame(
        data=np.array([
            game_clock,
            shot_clock,
            period,
            team_ids,
            player_ids,
            player_jersey,
            x_loc,
            y_loc
        ]).T,
        columns=headers)

    return mock_df


class TestPlayAnimation(unittest.TestCase):
    """Tests for play_animation.py"""

    def test_get_fixedtime(self):
        mock_df = make_mock_df()

        df = pa.get_fixedtime_df(
            period=1,
            time_start=14,
            time_end=13,
            dataframe=mock_df
        )
        self.assertEqual(df.shape[0], 10)
        np.testing.assert_array_equal(
            df.team_id.values,
            np.tile([-1, 100, 100, 222, 222], 2)
        )
        np.testing.assert_array_equal(df.period.values, 1)
        np.testing.assert_array_equal(df.game_clock.values >= 13, True)
        np.testing.assert_array_equal(df.game_clock.values <= 14, True)

        np.testing.assert_array_equal(df.period.values != 1, False)
        np.testing.assert_array_equal(df.game_clock.values < 13, False)
        np.testing.assert_array_equal(df.game_clock.values > 14, False)

    def test_team_coord(self):
        mock_df = make_mock_df()
        grouped_mock_df = mock_df.groupby(['game_clock', 'shot_clock'])
        instance_array = grouped_mock_df.groups.keys()
        instance_array.sort(reverse=True)

        # choose random element in instance array
        df_grouped_value = grouped_mock_df.get_group(instance_array[3])

        x_home, y_home, jersey_home = pa.team_coord(
            team_id=100,
            df_grouped_value=df_grouped_value
        )

        x_away, y_away, jersey_away = pa.team_coord(
            team_id=222,
            df_grouped_value=df_grouped_value
        )

        x_ball, y_ball, ball_id = pa.team_coord(
            team_id=-1,
            df_grouped_value=df_grouped_value
        )

        self.assertEqual(x_home.shape[0], 2)
        self.assertEqual(y_home.shape[0], 2)
        self.assertEqual(jersey_home.shape[0], 2)
        self.assertEqual(x_away.shape[0], 2)
        self.assertEqual(y_away.shape[0], 2)
        self.assertEqual(jersey_away.shape[0], 2)
        self.assertEqual(x_ball.shape[0], 1)
        self.assertEqual(y_ball.shape[0], 1)
        self.assertEqual(ball_id.shape[0], 1)
        self.assertEqual(ball_id, -1)

        np.assert_array_equal(np.logical_and(x_home >= 47, x_home <= 94), True)
        np.assert_array_equal(np.logical_and(y_home >= 0, y_home <= 50), True)

        np.assert_array_equal(np.logical_and(x_away >= 47, x_away <= 94), True)
        np.assert_array_equal(np.logical_and(y_away >= 0, y_away <= 50), True)

        np.assert_array_equal(np.logical_and(x_ball >= 47, x_ball <= 94), True)
        np.assert_array_equal(np.logical_and(y_ball >= 0, y_ball <= 50), True)


if __name__ == '__main__':
    unittest.main()
