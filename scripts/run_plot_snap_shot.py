from triple_triple.plot_snap_shot import (
    plot_player_movement_gradient,
    plot_play_snap_shot
)
from triple_triple.nbastats_game_data import hometeam_id, awayteam_id
from triple_triple.startup_data import (
    get_df_raw_position_data,
    get_df_positions
)

# TODO: Fix legend in plot_play_snap_shot

df_positions = get_df_positions()
df_raw_position_data = get_df_raw_position_data()


if __name__ == '__main__':

    player = 'Dwyane Wade'
    period = 1
    time_start = 402
    time_end = 400

    plot_player_movement_gradient(df_raw_position_data, player, period, time_start, time_end, color='Blues')

    ######################
    period = 2
    time_start = 100
    time_end = 99
    title_text = 'Snap shot of MIA @ GSW \n January 11, 2016'

    plot_play_snap_shot(df_positions, period, time_start, time_end, hometeam_id, awayteam_id, title_text)
