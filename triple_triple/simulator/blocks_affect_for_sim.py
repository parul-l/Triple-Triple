def blocks_affect_on_taking_shot(shot_prob, blocks_prob):
    if shot_prob < blocks_prob:
        return shot_prob
    else:
        return shot_prob - blocks_prob


def blocks_affect_on_making_shot(shot_prob, blocks_prob):
    if shot_prob < blocks_prob:
        # probably should be 0 or close to 0
        return shot_prob
    else:
        return shot_prob - blocks_prob
