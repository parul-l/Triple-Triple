# To compare basketball-reference and nba.com,
# we format the names in the 'same' way but
# some discrepancies still exist


def remove_unwanted_char(some_string):
    return some_string.replace('.', '').replace('*', '')


def all_player_ids(player_info_list):
    player_ids = {}
    len_players = len(player_info_list)

    for i in range(len_players):
        player_ids[player_info_list[i][0]] = (
            player_info_list[i][1],   # last, first
            remove_unwanted_char(player_info_list[i][2]), # first last name
            int(player_info_list[i][4]), # From
            int(player_info_list[i][5]) # To
        )

    return player_ids
