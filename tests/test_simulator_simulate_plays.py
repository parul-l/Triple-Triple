import mock
import unittest
import triple_triple.class_game as class_game
import triple_triple.simulator.simulate_plays as sp

from tests.mock_class_player import create_player_instances_dict


class TestClassSimulatePlays(unittest.TestCase):
    """Tests for simulator.simulate_plays.py"""

    def test_update_play_number_etiher_idx(self):
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

    @unittest.skip
    def test_initiate_player_has_possession(self):
        players_offense_dict = create_player_instances_dict('off')
        relative_player_possession_prob_mock = mock.Mock()
        relative_player_possession_prob_mock.side_effect = [[0, 1], [0.0, 1.0]]
        relative_player_possession_prob_mock()
        relative_player_possession_prob_mock()
        method_to_mock = ('triple_triple.prob_player_possessions'
                          '.relative_player_possession_prob')

        with mock.patch(method_to_mock, relative_player_possession_prob_mock):
            sp.initiate_player_has_possession(players_offense_dict)
        #     
        # 
        # 
        # mock.Mock(return_value=[[0, 1], [0.0, 1.0]])
        # players_offense_dict = create_player_instances_dict('off')
        # sp.initiate_player_has_possession(players_offense_dict)
        
        # 
        # self.assertTrue(players_offense_dict[1].has_possession)


if __name__ == '__main__':
    unittest.main()
