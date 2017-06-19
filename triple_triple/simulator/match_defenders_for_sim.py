import copy
import numpy as np


def make_dict_deep_copy(teams_list):
    return copy.deepcopy(teams_list[0]), copy.deepcopy(teams_list[1])


def update_defense_params(offense_class, defender_class):
    defender_class.on_defense = True
    defender_class.defending_who = offense_class.player_id
    offense_class.defended_by = defender_class.player_id


def match_players_same_position(
    teams_list,
    unmatched_players_list
):
    players_offense_dict_copy, players_defense_dict_copy = \
        make_dict_deep_copy(unmatched_players_list)

    # match players using position
    for defender in players_defense_dict_copy.values():
        defender_id = defender.player_id
        # break up position in to list for cases such as 'F-G'
        defender_position = list(defender.position)
        try:
            match_player_id = next(
                player_class.player_id
                for player_class
                in players_offense_dict_copy.values()
                if not set(
                    list(player_class.position)).isdisjoint(defender_position)
                )
            teams_list[1][defender_id].court_region = \
                teams_list[0][match_player_id].court_region
            teams_list[1][defender_id].court_coord = \
                teams_list[0][match_player_id].court_coord

            # update on_defense and defender status
            update_defense_params(
                offense_class=teams_list[0][match_player_id],
                defender_class=teams_list[1][defender.player_id]
            )
            # remove the matched players
            del players_offense_dict_copy[match_player_id]
            del players_defense_dict_copy[defender_id]
        except:
            continue

    # return unmatched players
    return [players_offense_dict_copy, players_defense_dict_copy]


def closest_height_to_defender(defender_class, players_offense_dict):
    players = list(players_offense_dict.values())
    height_from_defender = [
        player.height - defender_class.height for player in players
    ]
    idx_closest_player = np.abs(np.array(height_from_defender)).argmin()

    return players[idx_closest_player].player_id


def match_players_height(teams_list, unmatched_players_list):
    players_offense_dict_copy, players_defense_dict_copy = \
        make_dict_deep_copy(unmatched_players_list)

    for defender in players_defense_dict_copy.values():
        closest_off_player_id = closest_height_to_defender(
            defender_class=defender, players_offense_dict=players_offense_dict_copy
        )
        teams_list[1][defender.player_id].court_region = \
            teams_list[0][closest_off_player_id].court_region
        teams_list[1][defender.player_id].court_coord = \
            teams_list[0][closest_off_player_id].court_coord

        # update on_defense and defender status
        update_defense_params(
            offense_class=teams_list[0][closest_off_player_id],
            defender_class=teams_list[1][defender.player_id]
        )

        # remove the matched players
        del players_defense_dict_copy[defender.player_id]
        del players_offense_dict_copy[closest_off_player_id]

    # return unmatched players
    return [players_offense_dict_copy, players_defense_dict_copy]


def match_players_random(teams_list, unmatched_players_list):
    players_offense_dict_copy, players_defense_dict_copy = \
        make_dict_deep_copy(unmatched_players_list)

    off_players_list = list(teams_list[0].values())

    for defender in players_defense_dict_copy.values():
        # choose random player
        idx = np.random.randint(len(off_players_list))
        off_player = off_players_list[idx]
        teams_list[1][defender.player_id].court_region = \
            teams_list[0][off_player.player_id].court_region
        teams_list[1][defender.player_id].court_coord = \
            teams_list[0][off_player.player_id].court_coord

        # update on_defense and defender status
        update_defense_params(
            offense_class=teams_list[0][off_player.player_id],
            defender_class=teams_list[1][defender.player_id]
        )

        # remove the matched players
        off_players_list.pop(idx)
        del players_defense_dict_copy[defender.player_id]
        del players_offense_dict_copy[off_player.player_id]

    # return unmatched players
    return [players_offense_dict_copy, players_defense_dict_copy]


def initiate_defense_player_positions(teams_list):
    # match players by position
    # unmatched_players = [players_defense_dict_copy, players_offense_dict_copy]
    unmatched_players_list = \
        match_players_same_position(
            teams_list=teams_list,
            unmatched_players_list=teams_list
        )

    # match remaining players by height
    unmatched_players_list = \
        match_players_height(
            teams_list=teams_list,
            unmatched_players_list=unmatched_players_list
        )

    # match remaining players randomly
    unmatched_players_list = \
        match_players_random(
            teams_list=teams_list,
            unmatched_players_list=unmatched_players_list
        )


def update_defense_player_positions(teams_list):
    players_offense_dict, players_defense_dict = teams_list[0], teams_list[1]
    for defender in players_defense_dict.values():
        off_player_id = defender.defending_who
        defender.court_region = players_offense_dict[off_player_id].court_region
        defender.court_coord = players_offense_dict[off_player_id].court_coord
