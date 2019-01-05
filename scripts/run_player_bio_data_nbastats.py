import triple_triple.data_generators.player_bio_nbastats_data as pbd_nba

if __name__ == '__main__':

    player_id_list = [203110, 202691, 201939, 101106, 201575]
    # from NBA stats:

    df_player_bio = \
        pbd_nba.get_player_bio_df(player_id_list=player_id_list)

    # only useful when you know you are using active players!
    active_players_url = 'http://www.nba.com/players/active_players.json'

    df_active_player_bio_info = \
        pbd_nba.get_active_player_bio_df(active_players_url)

    # Save file
    # df_player_bio.to_csv('triple_triple/data/player_bio_info_nbastats.csv')
