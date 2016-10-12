from collections import Counter
import random

from triple_triple.startup_data import get_df_pos_dist
from triple_triple.player_passing_habits import get_player_court_region_df


# TODO: create court image labeling the regions

df_pos_dist = get_df_pos_dist()
df_pos_dist_reg = get_player_court_region_df(df_pos_dist)

player_name = 'Chris Bosh'
df_player_region = list(df_pos_dist_reg[player_name].region)

def get_player_region_prob(player_name, df_pos_dist_reg):
    df_player_region = list(df_pos_dist_reg[player_name].region)
    total_moments = len(df_player_region)
    reg_prob = {}
    for region, count in Counter(df_player_region).items():
        reg_prob[region] = count/float(total_moments)
    return reg_prob

player_reg_prob = get_player_region_prob(player_name, df_pos_dist_reg)

reg_to_num = {
    'bench': 0,
    'back court': 1,
    'inside 3-point line': 2,
    'key': 3,
    'out of bounds': 4,
    'paint': 5,
    'perimeter':6
}  

def get_player_simulated_regions(player_name, player_reg_prob, no_sim=100):
    p = [prob for prob in player_reg_prob.values()]
    sim_reg = []
    for i in range(no_sim):
        sim_reg.append(np.random.choice(np.arange(7), p=p))
    return sim_reg

sim_reg = get_player_simulated_regions(player_name, player_reg_prob, no_sim=100)

def generate_rand_positions(pos_num, shooting_side):
    if pos_num == 0:
        # bench values are empty
        xy = np.empty(2)
        xy[:] = np.NaN
        return [xy[0], xy[1]]
    
    elif pos_num == 1:
        # back court
        if shooting_side == 'left':
            return [random.uniform(47, 94), random.uniform(0, 50)]
        elif shooting_side == 'right':
            return [random.uniform(0, 47), random.uniform(0,50)]
    
    elif pos_num == 2:
        # inside 3-point line
        # break down the region in to 5 components
        # randomly choose one of the components
        # generate coordinates in that component
        
        component = np.random.choice(np.arange(5), p = [0.2]*5)
        
        if component == 0:
            if shooting_side == 'left':
                return [random.uniform(0, 14), random.uniform(3, 19)]
            elif shooting_side == 'right':
                return [random.uniform(80, 94), random.uniform(3, 19)]    
        
        if component == 1:
            if shooting_side == 'left':
                return [random.uniform(0, 14), random.uniform(31, 47)]
            elif shooting_side == 'right':
                return [random.uniform(80, 94), random.uniform(31, 47
                
                )]    
                
        
    
    
    elif pos_num == 5:
        # paint
        if shooting_side == 'left':
            return [random.uniform(0, 19), random.uniform(19,31)]
        elif shooting_side == 'right':
            return [random.uniform(75, 94), random.uniform(19,31)]
