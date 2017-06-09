import numpy as np


def dist_two_points(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_closest_to_ball(players_dict, ball_class):
    player_id_list = []
    dist_to_ball = []

    for player_class in players_dict.values():
        player_id_list.append(player_class.player_id)
        dist_to_ball.append(
            dist_two_points(
                point1=ball_class.court_coord,
                point2=player_class.court_coord
            )
        )
    dist_to_ball = np.array(dist_to_ball)
    min_dist_idx = np.where(
        dist_to_ball == dist_to_ball.min()
    )[0]

    return [player_id_list[i] for i in min_dist_idx]


def who_gets_rebound(
    teams_list,
    ball_class
):
    players_offense_dict, players_defense_dict = teams_list[0], teams_list[1]

    closest_off_players = get_closest_to_ball(
        players_dict=players_offense_dict,
        ball_class=ball_class
    )
    closest_def_players = get_closest_to_ball(
        players_dict=players_defense_dict,
        ball_class=ball_class
    )
    off_reb_prob = [players_offense_dict[player].off_rebounds_poss for player in closest_off_players]
    def_reb_prob = [players_defense_dict[player].def_rebounds_poss for player in closest_def_players]

    # scale combined probability array
    prob_array = np.array(off_reb_prob + def_reb_prob) / sum(off_reb_prob + def_reb_prob)

    rebounder_id = np.random.choice(
        a=closest_off_players + closest_def_players,
        p=prob_array
    )
    try:
        return players_defense_dict[rebounder_id]
    except:
        return players_offense_dict[rebounder_id]


def update_rebound_params(
    teams_list,
    game_class,
    ball_class
):
    rebounder_class = who_gets_rebound(
        teams_list,
        ball_class
    )

    rebounder_class.has_possession = True

    if rebounder_class.on_defense:
        rebounder_class.def_rebounds += 1
        game_class.def_rebounds[rebounder_class.game_idx] += 1

    else:
        rebounder_class.off_rebounds += 1
        game_class.off_rebounds[rebounder_class.game_idx] += 1

    return rebounder_class
