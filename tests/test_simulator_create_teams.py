import mock
import unittest
import triple_triple.simulator.create_teams as ct
from collections import Counter

from tests.fixtures.mock_data_for_tests import (
    open_df_raw_position_data_region_snippet,
    open_df_possession_region_snippet,
    open_df_play_by_play_snippet,
    open_df_game_stats_snippet
)

class TestClassCreateTeams(unittest.TestCase):
    """Tests for simulator.create_teams.py"""

    def test_create_unique_team_class(self):
        team_id_list1 = [0, 1, 2]
        team_id_list2 = [0, 0, 2]
        mock_get_player_bio_df = mock.Mock()
        mock_create_player_class_instance = mock.Mock()

        method_to_mock_player_bio = \
            ('triple_triple.simulator.create_teams'
             '.get_player_bio_df')
        method_to_mock_player_instance = \
            ('triple_triple.simulator.create_teams'
             '.create_player_class_instance')

        with mock.patch(
            method_to_mock_player_bio,
            mock_get_player_bio_df
        ):
            with mock.patch(
                method_to_mock_player_instance, mock_create_player_class_instance
            ):
                ct.create_unique_team_class(team_id_list=team_id_list1)
                unique_team_id_dict = Counter(team_id_list1)
                mock_get_player_bio_df.assert_called_once()
                mock_create_player_class_instance.assert_called_once()
                self.assertEqual(first=len(unique_team_id_dict), second=3)

                ct.create_unique_team_class(team_id_list=team_id_list2)
                unique_team_id_dict = Counter(team_id_list2)
                self.assertEqual(first=len(unique_team_id_dict), second=2)

    def test_get_players_on_both_teams_no_duplicates(self):
        team0_class_dict = {
            1: 'player1',
            2: 'player2'
        }
        team1_class_dict = {
            3: 'player3',
            4: 'player4'
        }

        players_both_teams = ct.get_players_on_both_teams(
            team0_class_dict=team0_class_dict,
            team1_class_dict=team1_class_dict
        )
        self.assertFalse(players_both_teams)

    def test_get_players_on_both_teams_with_duplicates(self):
        team0_class_dict = {
            1: 'player1',
            2: 'player2'
        }
        team1_class_dict = {
            1: 'player1',
            4: 'player4'
        }

        players_both_teams = ct.get_players_on_both_teams(
            team0_class_dict=team0_class_dict,
            team1_class_dict=team1_class_dict
        )
        self.assertEqual(players_both_teams, [1])

    def test_update_duplicates_btw_teams_no_duplicates(self):
        team0_class_dict = {
            1: 'player1',
            2: 'player2'
        }
        team1_class_dict = {
            3: 'player3',
            4: 'player4'
        }

        ct.update_duplicates_btw_teams(
            team0_class_dict=team0_class_dict,
            team1_class_dict=team1_class_dict
        )

        self.assertEqual(len(team0_class_dict), 2)
        self.assertEqual(team0_class_dict.keys(), [1, 2])
        self.assertEqual(set(team0_class_dict.values()), {'player1', 'player2'})

    def test_update_duplicates_btw_teams_with_duplicates(self):
        team0_class_dict = {
            1: 'player1_team0',
            2: 'player2'
        }
        team1_class_dict = {
            1: 'player1_team1',
            4: 'player4'
        }

        method_to_mock = ('triple_triple.simulator.create_teams'
                          '.get_players_on_both_teams')
        mock_get_players_on_both_teams = mock.Mock(return_value=[1])
        with mock.patch(method_to_mock, mock_get_players_on_both_teams):
            ct.update_duplicates_btw_teams(
                team0_class_dict=team0_class_dict,
                team1_class_dict=team1_class_dict
            )
            self.assertEqual(
                first=team0_class_dict[1],
                second=team1_class_dict[1]
            )

    @unittest.skip('ppp_mock functions should be called three times')
    def test_update_offense_info(self):
        team0_class_dict = {
            1: 'player1',
            2: 'player2'
        }
        team1_class_dict = {
            1: 'player1',
            4: 'player4'
        }

        game_id_list = [1]

        df_raw_position_region = open_df_raw_position_data_region_snippet()
        df_possession_region = open_df_possession_region_snippet()
        df_game_stats = open_df_game_stats_snippet()

        with mock.patch.multiple(
            'triple_triple.prob_player_possessions',
            update_region_freq_matrix=mock.DEFAULT,
            update_region_prob_matrix=mock.DEFAULT,
            update_possession_prob=mock.DEFAULT,
            get_action_freq_matrix=mock.DEFAULT,
            get_action_prob_matrix=mock.DEFAULT,
            get_shooting_freq=mock.DEFAULT,
            get_shooting_prob=mock.DEFAULT,
            get_regional_shooting_freq=mock.DEFAULT,
            get_regional_shooting_prob=mock.DEFAULT
        ) as ppp_mocks:
            with mock.patch('triple_triple.player_possession_habits'
                            '.characterize_player_possessions', mock.DEFAULT):
                with mock.patch('triple_triple.player_defending_habits'
                                '.update_traditional_nba_stats', mock.DEFAULT):
                    ct.update_offense_info(
                        team0_class_dict=team0_class_dict,
                        team1_class_dict=team1_class_dict,
                        game_id_list=game_id_list,
                        df_raw_position_region=df_raw_position_region,
                        df_possession_region=df_possession_region,
                        df_game_stats=df_game_stats,
                    )
                    ppp_mocks['update_region_freq_matrix'].assert_called_once()
                    ppp_mocks['update_region_prob_matrix'].assert_called_once()
                    ppp_mocks['update_possession_prob'].assert_called_once()
                    ppp_mocks['get_action_freq_matrix'].assert_called_once()
                    ppp_mocks['get_action_prob_matrix'].assert_called_once()
                    ppp_mocks['get_shooting_freq'].assert_called_once()
                    ppp_mocks['get_shooting_prob'].assert_called_once()
                    ppp_mocks['get_regional_shooting_freq'].assert_called_once()
                    ppp_mocks['get_regional_shooting_prob'].assert_called_once()


    def test_repeat_player_info(self):
        player_id = 1
        count = np.random.randint(5)
        team0_class_dict = {
            1: 'player1',
            2: 'player2'
        }
        

if __name__ == '__main__':
    unittest.main()
