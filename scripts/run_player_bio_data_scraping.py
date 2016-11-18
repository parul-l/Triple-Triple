# This player bio info is obtained from two sources
# 1. NBA stats (very slow)
# 2. basketball-reference.com (possibly has errors)
# This script is by scraping

import triple_triple.data_generators.player_bio_data_webscraping as pbd_web
from triple_triple.startup_data import get_player_ids


player_ids = get_player_ids()

if __name__ == '__main__':

    df_player_bio = pbd_web.player_bio_scraped_df()
    df_player_bio = pbd_web.add_ids_to_player_bio(
        df_player_bio,
        player_ids,
        current_year=2016
    )

    # Save file
    # df_player_bio.to_csv('triple_triple/data/player_bio_info_scraping.csv')
