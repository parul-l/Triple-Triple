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
