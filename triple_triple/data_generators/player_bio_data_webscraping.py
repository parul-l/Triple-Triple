# This player bio info is obtained from two sources
# 1. NBA stats (very slow)
# 2. basketball-reference.com (possibly has errors)

############################################################
# From basketball-reference (total player list length: 4446)
# See NBA stats file for comparison
############################################################

from datetime import datetime, date, time
import string

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

from triple_triple.startup_data import get_player_ids


player_ids = get_player_ids()

def parse_data(url):
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    tables = soup.findChildren('table')
    my_table = tables[0]

    return my_table.findChildren(['tr'])

def remove_unwanted_char(some_string):
    new_string = some_string.replace('.', '')
    new_string = new_string.replace('*', '')
    return new_string

def player_bio_scraped_df():
    player_bio_info = []
    bad_rows = []       # non-player rows
    bad_character = []  # letters with no one

    # iterate through alphabet to get all players and bios
    # subtract 1 from 'from' and 'to' to match nba.com
    for c in string.ascii_lowercase:
        url = "http://www.basketball-reference.com/players/" + c + "/"

        try:
            rows = parse_data(url)
            for row in rows:
                name_cell = row.findChildren('th')
                cells = row.findChildren('td')

                try:
                    temp_list= [
                        remove_unwanted_char(name_cell[0].text),      # name
                        int(cells[0].text)-1,                         # from
                        int(cells[1].text)-1,                         # to
                        cells[2].text,                                # position
                        cells[3].text,                                # height
                        int(cells[4].text),                           # weight
                        datetime.strptime(cells[5].text, '%B %d, %Y') # birthday
                    ]                                                 
                    player_bio_info.append(temp_list)

                except:
                    bad_rows.append(row.text)
        except:
            bad_character.append(c)

    headers = [
        "Player Name",
        "From",
        "To",
        "Position",
        "Height",
        "Weight",
        "Birthdate"
    ]

    return pd.DataFrame(player_bio_info, columns=headers)

def add_ids_to_player_bio(df_player_bio, player_ids, current_year=2016):

    # match players from player_ids to player_bio_info
    # create a list to input player ids in the order that the players
    # appear in df_player_bio
    id_index =np.zeros(len(df_player_bio), int)

    # create lists for player_ids not found in df_player_bio
    no_match_idx_current_yr = []
    no_match_idx_player_year_else = []
    multiple_matches = []
    for_loop_not_working = {}

    for playerid, name_year in player_ids.items():
        try:
            idx_player_year = df_player_bio.loc[\
                                (df_player_bio['Player Name'] == name_year[1]) & (df_player_bio['From'] == name_year[2])].index

            # unique player names and years
            if len(idx_player_year) == 1:
                id_index[idx_player_year] = playerid

            # player not found based on name and year
            elif len(idx_player_year) == 0:

                # find index only based on player and not year
                idx_player= df_player_bio.loc[
                                (df_player_bio['Player Name'] == name_year[1])].index

                # if there is only one match, add it to the index list
                if len(idx_player) == 1:
                    id_index[idx_player] = playerid

                    # if there are 0 matches or more than one match
                    # check if the player's year is current year
                    # since current year 'from' isn't on basketball-reference?

                elif name_year[2] == current_year:
                    # add it to no_match based on current year
                    # playerid, name, from, to, position, height, weight, bday
                    no_match_idx_current_yr.append(
                        [playerid, 
                        name_year[1], 
                        name_year[2], 
                        name_year[3],'
                        NaN', 
                        'NaN', 
                        0, 
                        0]
                    )
                else:
                    # everything else if:
                    # 0 hits with name and year
                    # no unique hit or current year hit
                    # playerid, name, from, to, position, height, weight, bday
                    no_match_idx_player_year_else.append(
                        [playerid, 
                        name_year[1], 
                        name_year[2], 
                        name_year[3], 
                        'NaN', 
                        'NaN', 
                        0, 
                        0]
                    )
            else:
                # players with multiple hits for both name and year
                multiple_matches.append((idx, playerid, name_year))
        except:
            for_loop_not_working[playerid] = name_year

    # add player_ids to DataFrame
    df_player_bio.insert(0, 'Player_ID', id_index)

    # add players starting in 2016 that are not on basketball-reference.
    # sloppy way of doing it
    headers_current_yr = [
        "Player_ID",
        "Player Name",
        "From",
        "To",
        "Position",
        "Height",
        "Weight",
        "Birthdate"
    ]

    df_current_year = pd.DataFrame(no_match_idx_current_yr,
                                   columns=headers_current_yr)

    return df_player_bio.append(df_current_year, ignore_index=True)

if __name__ == '__main__':

    df_player_bio =  player_bio_scraped_df()
    df_player_bio = add_ids_to_player_bio(df_player_bio, player_ids,
                                          current_year=2016)

    # Save file
    # df_player_bio.to_csv('triple_triple/data/player_bio_info_scraping.csv')
