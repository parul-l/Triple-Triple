from triple_triple.player.player_possession_habits_new import (
    get_player_action_frequency
)


if __name__ == '__main__':
    distance_to_ball = 4
    possession_block = 7.5
 
 
    gameids = ['0021500639']
    playerids = [203081]
    date_range = ['2016-01-20', '2016-01-20']
    get_player_action_frequency(
        playerids=playerids,
        date_range=date_range,
        diff_possclock_action_clock=5
    )


    gameids = ['0021500018']
    date_range = ['2015-10-29', '2015-10-29']
    playerids = [202331] # Paul George
    get_player_action_frequency(
        playerids=playerids,
        date_range=date_range,
        diff_possclock_action_clock=5
    )
