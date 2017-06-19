from triple_triple.class_player import create_player_class_instance
from triple_triple.startup_data import get_game_player_dict


# file opens as strings
game_player_dict = get_game_player_dict()

if __name__ == '__main__':

    player_list = [2547, 2548]
    player_classes_dict = create_player_class_instance(
        player_list=player_list,
        game_player_dict=game_player_dict,
    )


## OLD ##
    # pickeled_file = os.path.join(DATASETS_DIR, 'player_instances_info.p')
    # 
    # with open(pickeled_file, 'rb') as a_file:
    #     data = pickle.load(a_file)
    # 
    #     player_list = data['player_list']
    #     all_players_poss_prob_dict = data['all_players_poss_prob_dict']
    #     all_players_outcome_prob_matrix_dict = data['all_players_outcome_prob_matrix_dict']
    # 
    # # create player instances from Player class
    # num_players = len(player_list)
    # playerid_list = []
    # teamid_list = []
    # player_info_dict = {}
    # 
    # for i in range(num_players):
    #     playerid_list.append(playerid_from_name(player_list[i], game_id_dict))
    #     teamid_list.append(game_id_dict[playerid_list[i]][2])
    # 
    #     player_info_dict["player{0}".format(i)] = Player(
    #         player_list[i],
    #         playerid_list[i],
    #         teamid_list[i],
    #         all_players_poss_prob_dict[player_list[i]],
    #         all_players_outcome_prob_matrix_dict[player_list[i]]
    #     )
    # 
    # player_instances_file = os.path.join(DATASETS_DIR, 'player_instances.p')
    # 
    # with open(player_instances_file, 'wb') as a_file:
    #     pickle.dump(player_info_dict, a_file)
