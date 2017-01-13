import triple_triple.player_possession_habits as pph
from triple_triple.team_shooting_side import initial_shooting_side

from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_game_id_dict,
    get_df_pos_dist,
    get_df_pos_dist_trunc,
    get_df_play_by_play,
)

"""
    Use this file to collect player possession dictionaries for each player in player list.

    The script 'all_players_prob_dict' uses these files to collect probabilities for each player and saves info as a dictionary to be used in player instances.

    These files, 'player_i_poss_dfs.json' can be deleted after all_players_prob_dict.py is run.
"""

reg_to_num = {
    'back court': 0,
    'mid-range': 1,
    'key': 2,
    'out of bounds': 3,
    'paint': 4,
    'perimeter': 5
}

game_id_dict = get_game_id_dict()

df_pos_dist = get_df_pos_dist()
df_pos_dist_trunc = get_df_pos_dist_trunc()
df_play_by_play = get_df_play_by_play()

df_pos_dist_reg = pph.get_player_court_region_df(
    df_pos_dist,
    initial_shooting_side,
    hometeam_id,
    awayteam_id
)
df_pos_dist_reg_trunc = pph.get_pos_trunc_df(df_pos_dist_reg)


if __name__ == '__main__':

    # all players in the game
    player_list = [value[0] for value in game_id_dict.values()]
    player_list.remove('ball')

    num_players = len(player_list)

    for i in range(num_players):
        player_name = player_list[i]
        player_number = str(i)

        player_possession_dict = pph.create_player_poss_dict(
            player_name,
            game_id_dict,
            df_pos_dist_trunc,
            hometeam_id,
            awayteam_id,
            initial_shooting_side,
            df_play_by_play,
            df_pos_dist_reg,
            t=10
        )

        # save file to use in run_simulate_player_positions
        filename = 'player' + player_number + 'poss_dfs.json'
        pph.save_player_poss_dict(filename, player_possession_dict)

    # plot_coord = plot_team_possession(df_pos_dist_trunc, 10,20, hometeam_id, awayteam_id, game_id_dict)
