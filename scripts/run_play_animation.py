import matplotlib.pyplot as plt
import triple_triple.play_animation as pa
from triple_triple.full_court import draw_court
from triple_triple.startup_data import (
    get_game_info_dict,
    get_df_raw_position_data,
)


game_info_dict = get_game_info_dict()
df_raw_position_data = get_df_raw_position_data()


if __name__ == '__main__':

    period = 2
    time_start = 330
    time_end = 329

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    # ax.set_xlim([0, 94])
    # ax.set_ylim([0, 50])

    anim = pa.play_animation(
        period=period,
        time_start=time_start,
        time_end=time_end,
        fig=fig,
        game_info_dict=game_info_dict,
        dataframe=df_raw_position_data
    )

    # anim.save('nba_play_animation.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
    plt.show()
    plt.ioff()

    # There is a glitch with these times, quarter 1
    # time_start = 394
    # time_end = 393
