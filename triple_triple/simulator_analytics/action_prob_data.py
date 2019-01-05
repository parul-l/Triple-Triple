import pandas as pd
import numpy as np

action_prob_dict = {
    'Draymond Green': np.array([
        [0.308, 0.692, 0.000],
        [0.778, 0.222, 0.000],
        [0.889, 0.111, 0.000],
        [0.875, 0.125, 0.000],
        [0.889, 0.000, 0.111],
        [1.000, 0.000, 0.000]
    ]),
    'Stephen Curry': np.array([
        [0.333, 0.667, 0.000],
        [0.611, 0.333, 0.056],
        [0.333, 0.667, 0.000],
        [0.837, 0.163, 0.000],
        [0.917, 0.083, 0.000],
        [1.000, 0.000, 0.000]
    ]),
    'Chris Bosh': np.array([
        [0.500, 0.500, 0.000],
        [0.654, 0.231, 0.115],
        [0.600, 0.400, 0.000],
        [0.688, 0.312, 0.000],
        [1.000, 0.000, 0.000],
        [1.000, 0.000, 0.000]
    ]),
    'Dwyane Wade': np.array([
        [0.500, 0.500, 0.000],
        [0.577, 0.423, 0.000],
        [0.889, 0.111, 0.000],
        [0.941, 0.059, 0.000],
        [1.000, 0.000, 0.000],
        [1.000, 0.000, 0.000]
    ])
}


def get_prob_df(player_name):
    cols = ['pass', 'shoot', 'turnover']
    df = pd.DataFrame(action_prob_dict[player_name], columns=cols)
    df['region'] = ['paint', 'mid_range', 'top_key',
                    'perimeter', 'back_court', 'out_of_bounds']
    return df
