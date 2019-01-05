# From NBA STATS (total player list length: 4186)
# Format has changed. PlayerID required
# See Web Scraping file for comparison and obtaining all players
#######################################################
import pandas as pd
import triple_triple.data_generators.get_data as gd

base_url = 'http://stats.nba.com/stats/commonplayerinfo'
params = {
    'GraphEndSeason': '2016-17',    # don't think this is needed
    'GraphStartSeason': '2016-17',  # don't think this is needed
    'LeagueID': '00',
    'SeasonType': 'Regular Season',
    # 'SeasonType': 'Playoffs'
    # 'GraphStat': 'PTS',           # used in old nba stats format?
    # 'MeasureType': 'Base',        # used in old nba stats format?
    # 'PerMode': 'PerGame',         # used in old nba stats format?
}


def height_in(height_string):
    try:
        height = int(height_string.split('-')[0]) * 12 + \
            int(height_string.split('-')[1])
        return height
    except:
        pass


def get_player_bio_df(player_id_list, base_url=base_url, params=params):
    player_bio_info = []
    bad_ids = []
    for player_id in player_id_list:
        try:
            # add playerid to params
            params['PlayerID'] = str(player_id)
            player_data = gd.get_data(base_url, params)
            info_list = player_data['resultSets'][0]['rowSet'][0]

            player_bio_info.append([
                info_list[0],               # id
                info_list[4],               # name
                info_list[22],              # from
                info_list[23],              # to
                info_list[13],              # jersey
                info_list[14],              # position
                info_list[10],              # height
                info_list[11],              # weight
                info_list[6],               # bday
            ])
        except:
            bad_ids.append(player_id)

    bio_headers = [
        'player_id',
        'player_name',
        'from',
        'to',
        'jersey',
        'position',
        'height',
        'weight',
        'birthdate'
    ]

    df_player_bio = pd.DataFrame(player_bio_info, columns=bio_headers)
    df_player_bio['height'] = df_player_bio['height'].apply(height_in)

    return df_player_bio


# Get active player info only
def get_active_player_bio_df(url):
    data = gd.get_data(url, {})
    player_bio_info = []

    for player_dict in data:
        player_bio_info.append([
            int(player_dict['personId']),
            player_dict['displayName'],
            player_dict['pos'],
            int(player_dict['heightFeet']) * 12 + \
            int(player_dict['heightInches']),
            int(player_dict['weightPounds'])
        ])

    bio_headers = [
        'player_id',
        'player_name',
        'position',
        'height',
        'weight',
    ]

    return pd.DataFrame(player_bio_info, columns=bio_headers)
