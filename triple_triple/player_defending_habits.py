from collections import Counter
import numpy as np
from triple_triple.data_generators.player_traditional_statistics import get_player_stats_df
from triple_triple.prob_player_possessions import (
    get_reg_to_num,
    get_action_to_num,
    get_prob_count_matrix
)

# show columns along one line
# pd.options.display.width = 100


def update_traditional_nba_stats(
        player_class,
        season='2015-16',
        season_type='Regular Season'
    ):
    df_player_stats = get_player_stats_df(
        season=season,
        season_type=season_type
    )
    player_id = player_class.player_id
    player_stats = df_player_stats.query('player_id==@player_id').iloc[0]
    player_class.steals_game = player_stats.steals
    player_class.blocks_game = player_stats.blks
    player_class.off_rebounds_game = player_stats.off_rebounds
    player_class.def_rebounds_game = player_stats.def_rebounds
    player_class.personal_fouls_game = player_stats.personal_fouls
    player_class.free_throw_pct_game = player_stats.free_throw_pct


def get_df_possession_defender(
    offense_players_dict,
    df_possession_region,
    df_raw_position_region,
    defender_team_id
):
    cols = [
        'period',
        'game_clock',
        'player_id',
        'player_name',
        'region',
        'x_loc',
        'y_loc',
        'dist_to_ball'
    ]

    df_other_team = df_raw_position_region.query('team_id==@defender_team_id')[cols]
    # get relevant columns and original indices before groupby
    rename_cols = [
        'period',
        'game_clock',
        'defender_id',
        'defender_name',
        'defender_region',
        'defender_x_loc',
        'defender_y_loc',
        'defender_ball_dist'
    ]

    df_other_team.columns = rename_cols

    # get closest to ball from other team
    df_defender = df_other_team\
        .loc[df_other_team
        .groupby(['period', 'game_clock'])['defender_ball_dist']
        .idxmin()]

    # merge two dataframes on period and game_clock
    for player_class in offense_players_dict.values():
        player_id_list = [x.player_id for x in offense_players_dict.values()]
        df_player = df_possession_region.query('player_id in @player_id_list')

    df_possession_defender = df_player.merge(
        df_defender,
        on=['period', 'game_clock']
    )

    return df_possession_defender


def get_num_possessions_defended(defender_id, df_possession_defender):
    shift_col = (
        df_possession_defender.defender_id.shift(1) !=
        df_possession_defender.defender_id)

    df_possession_defender['block'] = (shift_col).astype(int).cumsum()
    defender_poss = df_possession_defender.query('defender_id==@defender_id')

    return float(len(defender_poss.block.unique()))


def get_stats_per_possession(
    defender_class,
    df_possession_defender,
    game_id=None
):
    if game_id is not None:
        df_possession_defender = df_possession_defender.query('game_id==@game_id')

    num_poss_defended = get_num_possessions_defended(
        defender_id=defender_class.player_id,
        df_possession_defender=df_possession_defender
    )

    defender_class.steals_poss = defender_class.steals_game / num_poss_defended
    defender_class.blocks_poss = defender_class.blocks_game / num_poss_defended
    defender_class.off_rebounds_poss = defender_class.off_rebounds_game / num_poss_defended
    defender_class.def_rebounds_poss = defender_class.def_rebounds_game / num_poss_defended
    defender_class.personal_fouls_poss = defender_class.personal_fouls_game / num_poss_defended


def poss_result_on_defense(
    defender_class,
    df_possession_defender,
    game_id=None
):
    if game_id is not None:
        df_possession_defender = df_possession_defender.query('game_id==@game_id')

    query_params = 'defender_id==@defender_class.player_id and possession_end'
    action_dict = Counter(
        df_possession_defender
        .query(query_params)
        .action
        .values
    )

    total_action = float(sum(action_dict.values()))

    action_prob_dict = {
        'pass': action_dict['pass'] / total_action,
        'shoot': (action_dict['missed_shot'] + action_dict['shot']) / total_action,
        'turnover': action_dict['turnover'] / total_action
    }

    # action_array = np.array([
    #     action_dict['pass'],
    #     action_dict['missed_shot'] + action_dict['shot'],
    #     action_dict['turnover'],
    # ], dtype=float)
    #
    # # [pass, shoot, turnover]
    defender_class.poss_result_on_defense = action_prob_dict


def poss_result_on_defense_reg(
    defender_class,
    df_possession_defender,
    game_id=None
):
    if game_id is not None:
        df_possession_defender = df_possession_defender.query('game_id==@game_id')

    query_params = 'defender_id==@defender_class.player_id and possession_end'

    df_action_defender = df_possession_defender.query(query_params)
    reg = df_action_defender.defender_region.values
    action = df_action_defender.action.values

    # row = region, column = [pass, shoot, turnover]
    action_matrix = np.zeros((6, 3))

    for i in range(len(action)):
        action_matrix[
            get_reg_to_num(reg[i]), get_action_to_num(action[i])
        ] += 1

    defender_class.poss_result_on_defense_reg = \
        get_prob_count_matrix(action_matrix)


# defense_player_reg vs. offense_player_reg
def get_def_off_region_matrix(
    defender_class,
    df_possession_defender,
    game_id=None
):
    if game_id is not None:
        df_possession_defender = df_possession_defender.query('game_id==@game_id')

    df_player = df_possession_defender\
        .query('defender_id==@defender_class.player_id')

    # query on defender and player regions
    def_region = df_player.defender_region.values
    player_region = df_player.region.values

    # rows = defender region
    # columns = player_poss region
    defending_region_matrix = np.zeros((6, 6))
    for i in range(len(def_region)):
        defending_region_matrix[
            get_reg_to_num(def_region[i]), get_reg_to_num(player_region[i])
        ] += 1

    defender_class.def_off_region_matrix = \
        get_prob_count_matrix(defending_region_matrix)
