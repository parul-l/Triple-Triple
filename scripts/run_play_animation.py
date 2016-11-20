import matplotlib.pyplot as plt
from triple_triple.full_court import draw_court

import triple_triple.play_animation as pa
import triple_triple.data_generators.player_position_data as ppd

from triple_triple.nbastats_game_data import teams_playing
from triple_triple.startup_data import get_player_ids

from save_playbyplay import all_games_stats


player_ids = get_player_ids()

# January 11, 2016: MIA @ GSW
game_id = '0021500568'

if __name__ == '__main__':
    tracking_file = '/Users/pl/Downloads/' + game_id + '.json'

    data = ppd.open_json(tracking_file)
    game_id_dict = ppd.get_game_id_dict(data)
    hometeam_id, awayteam_id = teams_playing(game_id, all_games_stats)

    df_positions = ppd.get_player_positions_df(data, game_id_dict)

    period = 1
    time_start = 300
    time_end = 250
    #
    # # There is a glitch with these times, quarter 1
    # # time_start = 394
    # # time_end = 393

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    anim = pa.play_animation(
        fig=fig, period=period, time_start=time_start,
        time_end=time_end, hometeam_id=hometeam_id,
        awayteam_id=awayteam_id
    )
    # anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
    plt.show()
    plt.ioff()

    ####################

    # TODO game clock/shot clock/ball height need fixing
    # it doesn't remove the previous frame
    player = 'Chris Bosh'
    playerid = pa.playerid_from_name(player)

    fig = plt.figure(figsize=(15, 9))
    ax = fig.gca()
    ax = draw_court(ax)
    anim = pa.play_animation(
        fig=fig, period=period, time_start=time_start,
        time_end=time_end, hometeam_id=hometeam_id,
        awayteam_id=awayteam_id, player=player
    )

    # anim.save('play.m4v', fps=10, extra_args=['-vcodec', 'libx264'])
    plt.show()
    plt.ioff()
