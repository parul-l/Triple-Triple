from triple_triple.connection import get_connection



# CREATE shooting side table

def get_shooting_side_query(gameid: str):
    """
        For a given game, this function creates the AWS Athena query 
        to create a table that determines which side of the court each 
        team is shooting in each quarter.

        The query results are stored in 's3://nba-game-info/team_shooting_side'
        and is partitioned by the season and gameid.
    
    Parameters
    ----------
        gameid: `str`
    """
    return """
        CREATE TABLE team_shooting_side WITH (
            external_location = 's3://nba-game-info/team_shooting_side',
            format = 'PARQUET',
            partitioned_by = ARRAY['season', 'gameid'],
            parquet_compression = 'SNAPPY'
            
        ) AS (
        WITH first_bucket AS (
            SELECT 
                gameid
                , period
                , player1_team_id					AS teamid
                , CAST(SUBSTRING(pctimestring, 1, STRPOS(pctimestring, ':') - 1) AS TINYINT) * 60 +
                CAST(SUBSTRING(pctimestring, STRPOS(pctimestring, ':') + 1, LENGTH(pctimestring)) AS TINYINT) 
                                                    AS periodclock
            FROM nba.playbyplay
            WHERE gameid = {}
            AND score IS NOT NULL
            ORDER BY wctimestring ASC
            LIMIT 1
        )
        , first_shot_shooting_side AS (
            SELECT
                gameposition.season
                , gameposition.gameid
                , gameposition.eventid
                , gameposition.moment_num
                , gameposition.period
                , gameposition.periodclock          AS periodclock_position
                , first_bucket.periodclock          AS periodclock_playbyplay
                , ABS(gameposition.periodclock - first_bucket.periodclock) 
                                                    AS clock_diff
                , first_bucket.teamid
                , gameposition.x_coordinate         AS x_coordinate_ball
                , gameposition.y_coordinate         AS y_coordinate_ball
                , gameposition.z_coordinate         AS z_coordinate_ball
                , CASE 
                    WHEN gameposition.x_coordinate < 47 THEN 'left'
                    WHEN gameposition.x_coordinate > 47 THEN 'right'
                ELSE NULL END                      AS shooting_side          
            FROM nba.gameposition
            INNER JOIN first_bucket 
            ON gameposition.gameid = first_bucket.gameid 
            AND gameposition.period = first_bucket.period
            AND playerid = -1
            AND first_bucket.periodclock - 2 <= gameposition.periodclock 
            AND gameposition.periodclock <= first_bucket.periodclock + 2
            ORDER BY ABS(gameposition.periodclock - first_bucket.periodclock) ASC
            LIMIT 1
        )
        , team_period AS (
            SELECT DISTINCT
                playbyplay.gameid
                , playbyplay.period
                , gamelog.team_id                   AS teamid
            FROM nba.playbyplay
            INNER JOIN nba.gamelog
            ON nba.playbyplay.gameid = nba.gamelog.gameid
            WHERE gamelog.gameid = {}
        )
            SELECT
              gamelog.game_date
            , team_period.teamid
            , gamelog.team_abbreviation
            , team_period.period
            , CASE
                WHEN team_period.teamid = first_shot_shooting_side.teamid 
                  AND team_period.period IN (1, 2) THEN first_shot_shooting_side.shooting_side -- first half for first team
                WHEN team_period.teamid != first_shot_shooting_side.teamid 
                  AND team_period.period IN (3, 4)
                THEN first_shot_shooting_side.shooting_side -- second half for second team
                -- second half for first team
                WHEN team_period.teamid = first_shot_shooting_side.teamid
                  AND first_shot_shooting_side.shooting_side = 'left'
                  AND team_period.period IN (3, 4) THEN 'right'
                WHEN team_period.teamid = first_shot_shooting_side.teamid
                  AND first_shot_shooting_side.shooting_side = 'right'
                  AND team_period.period IN (3, 4) THEN 'left'
                -- first half for second team
                WHEN team_period.teamid != first_shot_shooting_side.teamid
                  AND first_shot_shooting_side.shooting_side = 'left'
                  AND team_period.period IN (1, 2) THEN 'right'
                WHEN team_period.teamid != first_shot_shooting_side.teamid
                  AND first_shot_shooting_side.shooting_side = 'right'
                  AND team_period.period IN (1, 2) THEN 'left'
                ELSE NULL 
                END                       AS shooting_side
            , CURRENT_TIMESTAMP           AS lastupdate_DTS
            , gamelog.season
            , gamelog.gameid
            FROM team_period
            LEFT JOIN first_shot_shooting_side
                ON  team_period.gameid = first_shot_shooting_side.gameid
            --  AND team_period.teamid = first_shot_shooting_side.teamid (only join on gameid so that shooting side/teamid not null when no match)
            LEFT JOIN nba.gamelog
                ON  gamelog.gameid = team_period.gameid
                AND gamelog.team_id = team_period.teamid       
        );
    """.format(gameid)

def create_shooting_side_table(gameid: str):
    """
        For a given game, this function calls to query to create 
        the AWS Athena query that creates a table that determines 
        which side of the court each team is shooting in each quarter.

        The query results are stored in 's3://nba-game-info/team_shooting_side'
        and is partitioned by the season and gameid.
    
    Parameters
    ----------
        gameid: `str`
    """    
    query = get_shooting_side_query(gameid=gameid)

    # open aws connection
    conn = get_connection()
    # execute query
    cursor = conn.cursor()
    cursor.execute(query)

