import copy
from collections import Counter

import triple_triple.player_defending_habits as pdh
import triple_triple.player_possession_habits as pph
import triple_triple.prob_player_possessions as ppp

from triple_triple.class_player import create_player_class_instance

from triple_triple.data_generators.player_bio_nbastats_data import get_player_bio_df

from triple_triple.startup_data import (
    get_df_raw_position_region,
    get_game_player_dict,
    get_df_play_by_play
)

from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play

df_raw_position_region = get_df_raw_position_region()
df_possession_region = pph.get_possession_df(
    dataframe=df_raw_position_region,
    has_ball_dist=2.0,
    len_poss=15
)

game_player_dict = get_game_player_dict()
df_play_by_play = get_df_play_by_play()
df_game_stats = parse_df_play_by_play(df_play_by_play)


def create_unique_team_class(team_id_list, game_player_dict=game_player_dict):
    unique_team_id_dict = Counter(team_id_list)
    df_player_bio = get_player_bio_df(
        player_id_list=unique_team_id_dict.keys()
    )

    team_class_dict = create_player_class_instance(
        player_list=unique_team_id_dict.keys(),
        game_player_dict=game_player_dict,
        df_player_bio=df_player_bio
    )

    return team_class_dict


def get_players_on_both_teams(
    team0_class_dict,
    team1_class_dict
):
    return list(
        set(team0_class_dict.keys()) &
        set(team1_class_dict.keys())
    )


def update_duplicates_btw_teams(
    team0_class_dict,
    team1_class_dict
):
    players_both_teams = get_players_on_both_teams(
        team0_class_dict=team0_class_dict,
        team1_class_dict=team1_class_dict
    )

    copy_team1 = copy.deepcopy(team1_class_dict)
    for player in players_both_teams:
        team0_class_dict[player] = copy_team1[player]


def update_offense_info(
    team0_class_dict,
    team1_class_dict,
    game_id_list,
    df_raw_position_region,
    df_possession_region,
    df_game_stats,
    season='2015-16',
    season_type='Regular Season'
):
    # combine dictionaries to update both dictionaries together
    combined_players_dict = copy.copy(team0_class_dict)
    # if there are duplicates, updated version is used in combined
    combined_players_dict.update(team1_class_dict)

    for player_class in combined_players_dict.values():
        # update region probability

        ppp.update_region_freq_matrix(
            player_class=player_class,
            game_id=game_id_list[0],
            game_player_dict=game_player_dict,
            df_raw_position_region=df_raw_position_region,
            player_possession=False,
            team_on_offense=True,
            team_on_defense=False,
            half_court=True
        )
        ppp.update_region_prob_matrix(
            player_class=player_class
        )

        # update df_possessions using NBA df_game_stats info
        df_possession = pph.characterize_player_possessions(
            game_id=game_id_list[0],
            player_class=player_class,
            df_possession=df_possession_region,
            df_game_stats=df_game_stats
        )

        # update possession probability
        ppp.update_possession_prob(
            player_class=player_class,
            df_possession=df_possession,
            game_id=None
        )

        # update action probabilities
        ppp.get_action_freq_matrix(
            player_class=player_class,
            df_possession=df_possession
        )
        ppp.get_action_prob_matrix(
            player_class=player_class
        )

        # update shooting_prob
        ppp.get_shooting_freq(
            player_class=player_class,
            df_game_stats=df_game_stats
        )
        ppp.get_shooting_prob(
            player_class=player_class
        )

        # update region_shooting_prob
        ppp.get_regional_shooting_freq(
            player_class=player_class,
            df_possession=df_possession
        )
        ppp.get_regional_shooting_prob(
            player_class=player_class
        )

        # update season steals/blocks per game
        pdh.update_traditional_nba_stats(
            player_class=player_class,
            # season=season,
            #season_type=season_type
        )

    # update duplicates between teams
    update_duplicates_btw_teams(
        team0_class_dict=team0_class_dict,
        team1_class_dict=team1_class_dict
    )


def update_defense_info(
    offense_players_dict,
    defense_players_dict,
    defender_team_id,
    game_idx,
    df_possession_region=df_possession_region,
    df_raw_position_region=df_raw_position_region,
):

    df_possession_defender_team0 = pdh.get_df_possession_defender(
        offense_players_dict=offense_players_dict,
        df_possession_region=df_possession_region,
        df_raw_position_region=df_raw_position_region,
        defender_team_id=defender_team_id
    )

    for player_class in defense_players_dict.values():
        # update game_idx
        player_class.game_idx = game_idx
        # update possession outcome when defending
        pdh.poss_result_on_defense(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team0,
            game_id=None
        )

        pdh.poss_result_on_defense_reg(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team0,
            game_id=None
        )

        pdh.get_stats_per_possession(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team0,
            game_id=None
        )

        pdh.get_def_off_region_matrix(
            defender_class=player_class,
            df_possession_defender=df_possession_defender_team0,
            game_id=None,
        )


def repeat_player_info(player_id, count, team_class_dict):
    # count - 1 since original included in count
    for i in range(count - 1):
        copied_dict = copy.deepcopy(team_class_dict)
        # add 2*i number of zeros to front of duplicated player_id
        # id = 123 becomes 12300, or 1230000, or 12300000, etc.
        new_key = int(str(player_id) + 2 * (i + 1) * '0')
        team_class_dict[new_key] = copied_dict[player_id]

        # update player_id in duplicated_player
        team_class_dict[new_key].player_id = new_key
    return team_class_dict


def update_all_repeated_players(team_id_list, team_class_dict):
    player_id_count = Counter(team_id_list)
    duplicated_players = {k:v for k, v in player_id_count.items() if v > 1}
    for player_id, count in duplicated_players.items():
        team_class_dict = repeat_player_info(
            player_id=player_id,
            count=count,
            team_class_dict=team_class_dict
        )


def get_complete_teams(
    team0_id_list,
    team1_id_list,
    game_id_list
):
    # create team dicts for unique player_ids
    team0_class_dict = create_unique_team_class(team0_id_list)
    team1_class_dict = create_unique_team_class(team1_id_list)

    team0_id = team0_class_dict[team0_id_list[0]].team_id
    team1_id = team1_class_dict[team1_id_list[0]].team_id

    update_offense_info(
        team0_class_dict,
        team1_class_dict,
        game_id_list,
        df_raw_position_region,
        df_possession_region,
        df_game_stats,
        season='2015-16',
        season_type='Regular Season'
    )

    # update team0
    update_defense_info(
        offense_players_dict=team1_class_dict,
        defense_players_dict=team0_class_dict,
        defender_team_id=team0_id,
        game_idx=0,
        df_possession_region=df_possession_region,
        df_raw_position_region=df_raw_position_region,
    )
    # update team1
    update_defense_info(
        offense_players_dict=team0_class_dict,
        defense_players_dict=team1_class_dict,
        defender_team_id=team1_id,
        game_idx=1,
        df_possession_region=df_possession_region,
        df_raw_position_region=df_raw_position_region,
    )

    # update repeated players
    update_all_repeated_players(team0_id_list, team0_class_dict)
    update_all_repeated_players(team1_id_list, team1_class_dict)

    return team0_class_dict, team1_class_dict
