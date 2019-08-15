# delete triple_triple/player_possession_habits.py
import logging
import os

from triple_triple.data_generators.create_views import (
    create_action_region_view,
    create_possession_view,
    create_action_region_view
)
from triple_triple.data_generators.get_data import (
    athena,
    check_table_exists,
    check_view_exists,
    copy_bucket_contents,
    execute_athena_query,
    get_bucket_content,
    list_for_sql,
    remove_bucket_contents,
    s3
)
from triple_triple.game.game_info import (
    get_gameid_given_player,
    get_date_given_gameid
)
from triple_triple.config import SQL_DIR

# initiate logger
logger = logging.getLogger()
logger.setLevel('INFO')


class PlayerActionFrequencyPerGame(object):
    def __init__(
        self,
        playerids: list,
        gameid: str,
        gamedate: str,
        destination_bucket: str = 'nba-game-info',
        diff_possclock_action_clock: int = 5
    ):

        self.playerids = playerids
        self.gameid = gameid
        self.gamedate = gamedate
        self.destination_bucket = destination_bucket
        self.diff_possclock_action_clock = diff_possclock_action_clock
        self.action_region_query = None
        self.s3keys = {}

    def get_query(self):
        query = """
            SELECT
                  season
                , gameid
                , event_action
                , region_code
                , court_region
                , COUNT(*)		AS action_region_frequency
                , playerid
                , gamedate
            FROM nba.vw_action_region
            WHERE gameid = '{}'
              AND playerid IN {}
              AND diff_possclock_actionclock < {}
            GROUP BY season, gameid, gamedate, playerid, event_action, region_code, court_region
        """.format(
            self.gameid,
            list_for_sql(self.playerids),
            self.diff_possclock_action_clock
        )

        # action_region query
        action_region_sql_path = os.path.join(SQL_DIR, 'create_table_template.sql')
        
        with open(action_region_sql_path) as f:
            self.action_region_query = f.read().format(
                'nba.player_action_frequency_tmp',  # table name
                's3://nba-game-info/player_action_frequency_tmp', # external location
                "ARRAY['playerid', 'gamedate']", # partition by
                query
            )

    def create_tmp_table(self):
        logger.info('Creating tmp table for player-action-region-frequency')
        # create tmp table
        self.s3keys['tmp_table_{}'.format(self.gameid)] = execute_athena_query(
            query=self.action_region_query,
            database='nba',
            output_filename='',
            boto3_client=athena
        )

    def move_tmp_to_final(self):
        # check tmp table exists
        if check_table_exists(
            database_name='nba',
            table_name='player_action_frequency_tmp',
            max_time=60
        ):
            # move to final table
            logger.info('Moving tmp to final destination')
            all_files = get_bucket_content(
                bucket_name=self.destination_bucket,
                prefix='player_action_frequency_tmp',
                delimiter=''
            )
            # copy bucket contents
            copy_bucket_contents(
                copy_source_keys=all_files,
                destination_bucket=self.destination_bucket,
                destination_folder='player_action_frequency',
                s3client=s3
            )

    def alter_table(self):
        for player in self.playerids:
            location = 's3://{}/player_action_frequency/playerid={}/gamedate={}'.format(
                self.destination_bucket,
                player,
                self.gamedate
            )
            alter_query = """
                ALTER TABLE nba.player_action_frequency ADD
                    PARTITION (
                        playerid = {},
                        gamedate = '{}'
                    )
                    LOCATION '{}';    
            """.format(player, self.gamedate, location)
        
            try:
                self.s3keys['alter_table_{}'.format(self.gameid)] = execute_athena_query(
                    query=alter_query,
                    database='nba',
                    output_filename='alter_table_{}'.format(self.gameid),
                    boto3_client=athena
                )

            except Exception as err:
                logger.error('Error adding row to table {}'.format(self.gameid))
                logger.error(err)
        
    def drop_tmp_table(self, table: str = 'player_action_frequency_tmp'):
        logger.info('Dropping tmp table for player-action-region-frequency')
        query = "DROP TABLE IF EXISTS nba.{}".format(table)
        # execute drop table query
        self.s3keys['drop_{}'.format(table)] = execute_athena_query(
            query=query,
            database='nba',
            output_filename='drop_table_{}'.format(table),
            boto3_client=athena
        )

    def cleanup(self):
        # tmp files
        keys_tmp = get_bucket_content(
            bucket_name=self.destination_bucket,
            prefix='player_action_frequency_tmp',
            delimiter=''
        )

        # delete tmp keys and update metadata
        for key in keys_tmp:
            remove_bucket_contents(
                bucket=self.destination_bucket,
                key=key,
                s3client=s3
            )

    def run(self):
        self.get_query()
        self.create_tmp_table()
        all_files = self.move_tmp_to_final()
        self.alter_table()
        self.drop_tmp_table()
        self.cleanup()        


def get_player_action_frequency(
        playerids: list,
        gameids: list = [],
        date_range: list = [], # format ['1970-01-01', '2099-06-25'],
        distance_to_ball: int = 4,  # square distance 
        possession_block: int = 7.5, # min consecutive blocks to consider a possession (0.8th of a second)
        diff_possclock_action_clock: int = 5,
        max_time: int = 60 # max time for vw_action_region to be made
):
    """
        This function requires either (i) a date range or (ii) list of gameids,
        to obtain player frequency data from either (i) or (ii) or the 
        intersection of both
    """
    if not date_range and not gameids:
        logger.error('Need to specify date_range OR gameids OR both.')

    if date_range:
        gameid_dates = get_gameid_given_player(
            players=playerids, date_range=date_range)
        if gameids:
            gameids = list(set(gameid_dates) & set(gameids))
        else:
            gameids = gameid_dates

    # create the action_region view
    execute_response = create_action_region_view(
        playerids=playerids,
        gameids=gameids,
        date_range=date_range,
        distance_to_ball=distance_to_ball,
        possession_block=possession_block
    )
    # make sure view exists
    vw_exists = check_view_exists(
        database='nba',
        view_name='vw_action_region',
        max_time=180
    )
    print(vw_exists)
    
    if vw_exists:
        for gameid in gameids:
            gamedate = get_date_given_gameid(gameid=gameid, max_time=10)
            etl = PlayerActionFrequencyPerGame(
                playerids=playerids,
                gameid=gameid,
                gamedate=gamedate,
            )
            etl.run()
    else:
        logger.info('vw_action_region does not exist')
        print('vw_action_region does not exist')

    # drop views (they are no longer needed)
    logger.info('Dropping possession-region view for given players')
    response_poss = execute_athena_query(
        query='DROP VIEW nba.vw_possession;',
        database='nba',
        output_filename='drop_poss_tmp_vw',
    )

    logger.info('Dropping court-region view for given players')
    response_drop_court = execute_athena_query(
        query='DROP VIEW nba.vw_courtregion;',
        database='nba',
        output_filename='drop_courtregion_vw',
    )

    logger.info('Dropping action-region view for given players')
    response_action_region = execute_athena_query(
        query='DROP VIEW nba.vw_action_region;',
        database='nba',
        output_filename='drop_action_region_vw',
    )    

