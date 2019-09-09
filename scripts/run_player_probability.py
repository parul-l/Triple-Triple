from triple_triple.player.player_probability import (
    player_action_frequency_per_game,
    get_player_probability
)


if __main__ == '__name__':
    gameids = ['0021500020']
    date_range = ['2015-10-29', '2015-10-29']
    playerid = 1717 # Dirk Nowitzki


    df_player_freq = player_action_frequency_per_game(
        playerid=playerid,
        date_range=date_range,
        gameids=gameids
    )

    df_player_prob = get_player_probability(player_action_frequency=df_player_freq)