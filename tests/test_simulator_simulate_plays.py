import mock
import unittest
import triple_triple.class_game as class_game
import triple_triple.simulator.simulate_plays as sp

from tests.mock_class_player import (
    create_player_instances_dict,
    create_ball_class
)


class TestClassSimulatePlays(unittest.TestCase):
    """Tests for simulator.simulate_plays.py"""

    def test_update_play_number_either_idx(self):
        game_class = class_game.Game(
            hometeam_id=0000,
            awayteam_id=1111
        )
        assert game_class.num_plays == [0, 0]
        # test first index
        sp.update_play_number(game_class=game_class, off_game_idx=0)

        self.assertEqual(
            first=game_class.num_plays,
            second=[1, 0]
        )
        # test second index
        sp.update_play_number(game_class=game_class, off_game_idx=1)
        self.assertEqual(
            first=game_class.num_plays,
            second=[1, 1]
        )

    def test_switch_team_possession_list_switch(self):
        teams_list_before = [
            create_player_instances_dict('off'),
            create_player_instances_dict('def')
        ]

        teams_list_after = sp.switch_team_possession(teams_list=teams_list_before)

        assert teams_list_before[0] == teams_list_after[1]
        assert teams_list_before[1] == teams_list_after[0]

    def test_switch_team_possession_player_param_swap(self):
        teams_list_before = [
            create_player_instances_dict('off'),
            create_player_instances_dict('def')
        ]

        for player in teams_list_before[0].values():
            assert player.on_offense is True
            assert player.on_defense is False

        for player in teams_list_before[1].values():
            assert player.on_offense is False
            assert player.on_defense is True

        teams_list_after = sp.switch_team_possession(teams_list=teams_list_before)

        for player in teams_list_after[1].values():
            self.assertFalse(player.on_offense)
            self.assertTrue(player.on_defense)

        for player in teams_list_after[0].values():
            self.assertTrue(player.on_offense)
            self.assertFalse(player.on_defense)

    def test_switch_shooting_side(self):
        self.assertEqual(
            first=sp.switch_shooting_side(['left', 'right']),
            second=['right', 'left']
        )

        self.assertEqual(
            first=sp.switch_shooting_side(['right', 'left']),
            second=['left', 'right']
        )

    def test_who_has_possession_one_person(self):
        players_offense_dict = create_player_instances_dict('off')

        players_offense_dict[0].has_possession = True

        self.assertEqual(
            first=sp.who_has_possession(players_offense_dict),
            second=players_offense_dict[0]
        )

    def test_who_has_possession_no_one(self):
        players_offense_dict = create_player_instances_dict('off')

        with self.assertRaises(ValueError):
            self.assertRaises(
                sp.who_has_possession(players_offense_dict=players_offense_dict)
            )

    def test_who_has_possession_more_than_one(self):
        players_offense_dict = create_player_instances_dict('off')

        players_offense_dict[0].has_possession = True
        players_offense_dict[1].has_possession = True

        with self.assertRaises(ValueError):
            self.assertRaises(
                sp.who_has_possession(players_offense_dict=players_offense_dict)
            )

    def test_initiate_player_has_possession(self):
        players_offense_dict = create_player_instances_dict('off')
        # method_to_mock = ('triple_triple.prob_player_possessions'
        #                   '.relative_player_possession_prob')

        # with mock.patch(method_to_mock, relative_player_possession_prob_mock):
        #     sp.initiate_player_has_possession(players_offense_dict)

        sp.relative_player_possession_prob = \
            mock.Mock(return_value=[[0, 1], [0.0, 1.0]])
        sp.initiate_player_has_possession(players_offense_dict)

        self.assertTrue(players_offense_dict[1].has_possession)
        self.assertFalse(players_offense_dict[0].has_possession)
        self.assertEqual(
            first=sp.who_has_possession(players_offense_dict),
            second=players_offense_dict[1]
        )

    def test_update_ball_position_out_of_bounds(self):
        ball_class = create_ball_class()
        reg_to_num = {
            'paint': 0,
            'mid-range': 1,
            'key': 2,
            'perimeter': 3,
            'back_court': 4,
            'out_of_bounds': 5
        }
        mock_get_reg_to_num = mock.Mock(return_value=reg_to_num)

        method_to_mock = ('triple_triple.prob_player_possessions'
                          '.get_reg_to_num')

        with mock.patch(method_to_mock, mock_get_reg_to_num):
            sp.update_ball_position(
                shooting_side='right',
                out_of_bounds=True,
                ball_class=ball_class
            )

        self.assertEqual(
            first=ball_class.court_region,
            second=reg_to_num['out_of_bounds']
        )
        self.assertEqual(
            first=ball_class.court_coord,
            second=[96, 25]
        )
        with mock.patch(method_to_mock, mock_get_reg_to_num):
            sp.update_ball_position(
                shooting_side='left',
                out_of_bounds=True,
                ball_class=ball_class
            )

        self.assertEqual(
            first=ball_class.court_region,
            second=reg_to_num['out_of_bounds']
        )
        self.assertEqual(
            first=ball_class.court_coord,
            second=[-2, 25]
        )

    def test_update_ball_position_no_has_ball_class(self):
        ball_class = create_ball_class()
        reg_to_num = {
            'paint': 0,
            'mid-range': 1,
            'key': 2,
            'perimeter': 3,
            'back_court': 4,
            'out_of_bounds': 5
        }
        mock_get_reg_to_num = mock.Mock(return_value=reg_to_num)

        method_to_mock = ('triple_triple.prob_player_possessions'
                          '.get_reg_to_num')

        with mock.patch(method_to_mock, mock_get_reg_to_num):
            sp.update_ball_position(
                shooting_side='right',
                ball_class=ball_class
            )

        self.assertEqual(
            first=ball_class.court_region,
            second=reg_to_num['paint']
        )
        self.assertEqual(
            first=ball_class.court_coord,
            second=[88.75, 25]
        )

        with mock.patch(method_to_mock, mock_get_reg_to_num):
            sp.update_ball_position(
                shooting_side='left',
                ball_class=ball_class
            )

            self.assertEqual(
                first=ball_class.court_region,
                second=reg_to_num['paint']
            )
            self.assertEqual(
                first=ball_class.court_coord,
                second=[5.25, 25]
            )

    def test_update_ball_position_has_ball_class(self):
        players_offense_dict = create_player_instances_dict('off')
        ball_class = create_ball_class()

        players_offense_dict[0].has_possession = True
        players_offense_dict[0].court_region = 'test_region'
        players_offense_dict[0].court_coord = [23.0, 48]

        sp.update_ball_position(
            shooting_side='right/left',
            has_ball_class=players_offense_dict[0],
            ball_class=ball_class
        )

        self.assertEqual(
            first=ball_class.court_region,
            second=players_offense_dict[0].court_region
        )
        self.assertEqual(
            first=ball_class.court_coord,
            second=players_offense_dict[0].court_coord
        )

    def test_initiate_offense_player_positions_functions_called(self):
        players_dict = create_player_instances_dict('off')
        # choose random player to have possession of ball
        players_dict[0].has_possession = True
        has_ball_class = players_dict[0]
        shooting_side = 'right'

        with mock.patch.multiple(
            'triple_triple.simulator.simulate_plays',
            update_ball_position=mock.DEFAULT,
            update_offense_player_positions=mock.DEFAULT
        ) as mocks:
            sp.initiate_offense_player_positions(
                players_offense_dict=players_dict,
                shooting_side=shooting_side
            )
            mocks['update_offense_player_positions'].assert_called_once_with(
                players_offense_dict=players_dict,
                shooting_side=shooting_side,
                num_reg=6
            )
            mocks['update_ball_position'].assert_called_once_with(
                shooting_side=shooting_side,
                out_of_bounds=True
            )

            self.assertEqual(
                sp.who_has_possession(players_offense_dict=players_dict),
                has_ball_class
            )

            self.assertEqual(
                first=sp.get_reg_to_num('out_of_bounds'),
                second=has_ball_class.court_region
            )

            self.assertEqual(
                first=sp.generate_rand_regions(
                    court_region_num=has_ball_class.court_region,
                    shooting_side=shooting_side
                ),
                second=has_ball_class.court_coord
            )


if __name__ == '__main__':
    unittest.main()
