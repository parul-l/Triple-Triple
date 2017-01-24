import pandas as pd
import numpy as np


def get_overlap_idx_play_by_play(df_play_by_play):
    # indices with both HOMEDESCRIPTION and VISITORDESCRIPTION
    overlapping_idx = []
    for i in range(len(df_play_by_play)):
        if (not pd.isnull(df_play_by_play.VISITORDESCRIPTION.iloc[i])) and (not pd.isnull(df_play_by_play.HOMEDESCRIPTION.iloc[i])):
            overlapping_idx.append(i)
    return overlapping_idx


def get_descrip_df(df_play_by_play, DESCRIPTION):
        return df_play_by_play[df_play_by_play[DESCRIPTION].notnull()]


def get_descrip_split(df_descrip, DESCRIPTION):
    return [row.replace('(', '').replace(')', '').split()
            for row in df_descrip[DESCRIPTION].values]


def get_df_and_descrip_splits_for_parsing(df_play_by_play):
    overlapping_idx = get_overlap_idx_play_by_play(df_play_by_play)

    df_descrip_home = get_descrip_df(df_play_by_play, 'HOMEDESCRIPTION')
    df_descrip_visitor = get_descrip_df(df_play_by_play, 'VISITORDESCRIPTION')
    descrip_visitor_idx = df_descrip_visitor.index.values

    # remove the overlapping_idx with HOMEDESCRIPTION
    descrip_visitor_idx = list(set(descrip_visitor_idx) - set(overlapping_idx))
    df_descrip_visitor = df_descrip_visitor.ix[descrip_visitor_idx]

    descrip_split_home = get_descrip_split(df_descrip_home, 'HOMEDESCRIPTION')
    descrip_split_visitor = get_descrip_split(df_descrip_visitor, 'VISITORDESCRIPTION')

    # convert 'HOMEDESCRIPTION' and 'VISITORDESCRIPTION' columns in
    # opposite dataframes to strings.
    # used to check MISSED blocks

    df_descrip_home.loc[:, 'VISITORDESCRIPTION'] = df_descrip_home['VISITORDESCRIPTION'].astype(str)

    df_descrip_visitor.loc[:, 'HOMEDESCRIPTION'] = df_descrip_visitor['HOMEDESCRIPTION'].astype(str)

    return df_descrip_home, df_descrip_visitor, descrip_split_home, descrip_split_visitor


def get_idx_for_parsing_play_by_play(df_play_by_play):

    df_descrip_home, df_descrip_visitor, descrip_split_home, descrip_split_visitor = get_df_and_descrip_splits_for_parsing(df_play_by_play)

    # separate indices that start with MISS
    home_miss_idx = [i for i, x in enumerate(descrip_split_home) if x[0] == 'MISS']
    home_other_idx = list(set(range(len(descrip_split_home))) - set(home_miss_idx))

    visitor_miss_idx = [i for i, x in enumerate(descrip_split_visitor) if x[0] == 'MISS']
    visitor_other_idx = list(set(range(len(descrip_split_visitor))) - set(visitor_miss_idx))

    return [home_other_idx, home_miss_idx, visitor_other_idx, visitor_miss_idx]


def add_poss_to_action_list(idx, action_list, df_descrip, action, player_num, other_note, description):
    player_id = 'PLAYER' + str(player_num) + '_ID'
    player_name = 'PLAYER' + str(player_num) + '_NAME'
    action_list.append([
        df_descrip.iloc[idx]['PERIOD'],         # PERIOD
        df_descrip.iloc[idx]['PCTIMESTRING'],   # GAME CLOCK
        df_descrip.iloc[idx][player_id],        # PLAYER_ID
        df_descrip.iloc[idx][player_name],      # PLAYER_NAME
        action,                                 # ACTION
        other_note,                             # OTHER_NOTE
        df_descrip.iloc[idx][description],      # NBA DESCRIPTION
    ])

    return action_list


def parse_descrip(df_descrip, descrip_split, idx_list, action_list, description):
    # separate index type:
    other_idx = idx_list[0]
    miss_idx = idx_list[1]

    for idx in other_idx:
        # Check REBOUND:
        if descrip_split[idx][1] == 'REBOUND':
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='rebound',
                player_num=1,
                other_note=descrip_split[idx][-2:],
                description=description
            )

        # Check committed FOUL:
        elif descrip_split[idx][1][-4:] == 'FOUL':
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='committed_foul',
                player_num=1,
                other_note=descrip_split[idx][1],
                description=description
            )

        # Check TURNOVER
        elif 'Turnover' in descrip_split[idx]:
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='turnover',
                player_num=1,
                other_note=None,
                description=description
            )

        # Check Made FREE THROW
        elif 'Free Throw' in ' '. join(descrip_split[idx]):
            if 'Technical' in descrip_split:
                other_note = 'technical'
            else:
                other_note = None

            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='free_throw',
                player_num=1,
                other_note=other_note,
                description=description
            )

        # Check STEAL/TURNOVER:
        elif descrip_split[idx][1] == 'STEAL':
            # add steal
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='steal',
                player_num=2,
                other_note=None,
                description=description
            )
            # add turnover
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='turnover',
                player_num=1,
                other_note='stolen',
                description=description
            )

        # Check BLOCK/MISSED SHOT
        elif descrip_split[idx][1] == 'BLOCK':
            # add block
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='block',
                player_num=3,
                other_note=df_descrip.iloc[idx].PLAYER1_NAME,
                description=description
            )
            # add attempted shot
            if '3PT' in descrip_split[idx]:
                other_note = 3
            else:
                other_note = 2
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='shot',
                player_num=1,
                other_note=other_note,
                description=description
            )
        # Check MADE SHOT w or w/o ASSIST:
        elif 'PTS' in descrip_split[idx]:
            # check 2 or 3
            if '3PT' in descrip_split[idx]:
                other_note = 3
            else:
                other_note = 2

            # add shot
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='shot',
                player_num=1,
                other_note=other_note,
                description=description
            )

            # check ASSIST
            if 'AST' in descrip_split[idx]:
                add_poss_to_action_list(
                    idx=idx,
                    action_list=action_list,
                    df_descrip=df_descrip,
                    action='assist',
                    player_num=2,
                    other_note=None,
                    description=description
                )

    for idx in miss_idx:
        # Check MISSED Free Throws
        if 'Free Throw' in ' '. join(descrip_split[idx]):
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='free_throw',
                player_num=1,
                other_note=0,
                description=description
            )

        # Check MISSED SHOT/BLOCK
        elif ('BLOCK' in df_descrip.iloc[idx]['HOMEDESCRIPTION']) or \
             ('BLOCK' in df_descrip.iloc[idx]['VISITORDESCRIPTION']):

            # add block
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='block',
                player_num=3,
                other_note=df_descrip.iloc[idx].PLAYER1_NAME,
                description=description
            )

        else:
            # add attempted shot
            if '3PT' in descrip_split[idx]:
                other_note = 3
            else:
                other_note = 2
            add_poss_to_action_list(
                idx=idx,
                action_list=action_list,
                df_descrip=df_descrip,
                action='missed_shot',
                player_num=1,
                other_note=other_note,
                description=description
            )

    return action_list


def parse_df_play_by_play(df_play_by_play):
    idx_list = get_idx_for_parsing_play_by_play(df_play_by_play)

    df_descrip_home, df_descrip_visitor, descrip_split_home, descrip_split_visitor = get_df_and_descrip_splits_for_parsing(df_play_by_play)

    action_list = []

    # parse home data
    action_list = parse_descrip(
        df_descrip=df_descrip_home,
        descrip_split=descrip_split_home,
        idx_list=[idx_list[0], idx_list[1]],
        action_list=action_list,
        description='HOMEDESCRIPTION'
    )

    # parse visitor data
    action_list = parse_descrip(
        df_descrip=df_descrip_visitor,
        descrip_split=descrip_split_visitor,
        idx_list=[idx_list[2], idx_list[3]],
        action_list=action_list,
        description='VISITORDESCRIPTION'
    )

    column_headers = [
        'period',
        'game_clock',
        'player_id',
        'player_name',
        'action',
        'other_note',
        'descrip'
    ]

    df_descrip_parsed = pd.DataFrame(data=action_list, columns=column_headers)
    # add game_id column
    game_id_col = np.full(
        shape=len(df_descrip_parsed), fill_value=df_play_by_play.loc[0]['Game_ID'],
        dtype=int
    )
    df_descrip_parsed['game_id'] = game_id_col

    return df_descrip_parsed.sort(['period', 'game_clock'], ascending=[True, False])
