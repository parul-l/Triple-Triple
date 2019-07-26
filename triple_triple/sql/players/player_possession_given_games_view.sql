CREATE VIEW nba.vw_poss_tmp AS
    WITH closest AS (
        SELECT
            season
        , gameid
        , eventid
        , moment_num
        , timestamp_dts
        , timestamp_utc
        , period
        , periodclock
        , shotclock
        , teamid
        , playerid
        , x_coordinate
        , y_coordinate
        , z_coordinate
        , distance_from_ball_sq
        , closest_to_ball_rank
        FROM nba.closest_to_ball
        WHERE gameid IN {0}
        AND closest_to_ball_rank = 1 
        AND distance_from_ball_sq <= {1} -- distance squared
    )
    , shifted_closest_player AS (
        SELECT
            season
        , gameid
        , eventid
        , moment_num
        , playerid
        , CASE WHEN 
            LAG(playerid, 1, playerid) OVER (ORDER BY season, gameid, eventid, moment_num) = playerid 
            THEN 0 ELSE 1 END               AS is_different_player_is_closest           
        FROM closest
    )
    /* this enumerates the blocks */
    , possession_blocks AS (
        SELECT 
            season
        , gameid
        , eventid
        , moment_num
        , playerid
        , SUM(is_different_player_is_closest) OVER (ORDER BY season, gameid, eventid, moment_num) 
                                            AS enumerated_blocks
        FROM shifted_closest_player
    )
    , length_possession_block AS (
        SELECT
        playerid
        , enumerated_blocks
        , COUNT(*)	                    AS possession_length
        FROM possession_blocks
        GROUP BY playerid, enumerated_blocks	
    )
        SELECT      
            closest.season
        , closest.gameid
        , closest.eventid
        , closest.moment_num
        , closest.timestamp_dts
        , closest.timestamp_utc
        , closest.period
        , closest.periodclock
        , closest.shotclock
        , closest.teamid
        , closest.playerid
        , closest.x_coordinate
        , closest.y_coordinate
        , closest.z_coordinate
        , closest.distance_from_ball_sq
        , length_possession_block.enumerated_blocks
        , length_possession_block.possession_length
        , CASE WHEN 
                length_possession_block.possession_length >= {2} 
            THEN 1 ELSE 0 END               AS has_ball
        , vw_courtregion.court_region
        FROM closest
        LEFT JOIN possession_blocks USING (season, gameid, eventid, moment_num, playerid)
        LEFT JOIN length_possession_block 
            ON  possession_blocks.playerid = length_possession_block.playerid
            AND possession_blocks.enumerated_blocks = length_possession_block.enumerated_blocks
        INNER JOIN nba.vw_courtregion 
            ON  vw_courtregion.season = closest.season
            AND vw_courtregion.gameid = closest.gameid
            AND vw_courtregion.eventid = closest.eventid
            AND vw_courtregion.moment_num = closest.moment_num
            AND vw_courtregion.playerid = closest.playerid
        WHERE length_possession_block.possession_length >= {2} -- this implies player has possession
        ORDER BY season, gameid, eventid, moment_num, length_possession_block.enumerated_blocks
