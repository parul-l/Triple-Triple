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

        teams_list_after = sp.switch_team_possession(teams_list=teams_list_before)

        for player in teams_list_after[1].values():
            self.assertFalse(player.on_offense)
            self.assertTrue(player.on_defense)


if __name__ == '__main__':
    unittest.main()
