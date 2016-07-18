import numpy as np

#############
# player has ball
############

def player_has_ball(x_player, y_player, x_ball, y_ball):
    dist = np.linalg.norm(np.array((x_player, y_player))-
                        np.array((x_ball, y_ball)))
    if dist <=1:
        return True
    else:
        return False
    
