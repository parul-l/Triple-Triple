/*
Joining relevant_gameids to closest scans more data
then using a WHERE clause for the gameids.
Consequently, use player_possession_habits.get_gameid_given_players
first and then run player_possession_given_gameids.sql
*/

WITH relevant_games AS (
    SELECT DISTINCT gameid
    FROM nba.playerinfo
    WHERE playerid IN {}
    AND gameid = '0021500639' -- add for now for sake of $$
    -- WHERE playerid IN (202714, 201952)
)
, closest AS (
    SELECT
        season
      , relevant_games.gameid
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
    INNER JOIN relevant_games 
      ON closest_to_ball.gameid = relevant_games.gameid
    WHERE closest_to_ball_rank = 1 
    AND distance_from_ball_sq <= {} -- distance squared
    -- AND eventid = 53
    -- AND moment_num BETWEEN 3 AND 60
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
	  , length_possession_block.possession_length
      , CASE WHEN 
            length_possession_block.possession_length >= {} 
        THEN 1 ELSE 0 END               AS has_ball          

    FROM closest
      LEFT JOIN possession_blocks USING (season, gameid, eventid, moment_num, playerid)
            -- ON  possession_blocks.season = closest.season
            -- AND possession_blocks.gameid = closest.gameid
            -- AND possession_blocks.eventid = closest.eventid
            -- AND possession_blocks.moment_num = closest.moment_num
            -- AND possession_blocks.playerid = closest.playerid
      LEFT JOIN length_possession_block USING (playerid, enumerated_blocks)
        -- ON  possession_blocks.playerid = length_possession_block.playerid
        -- AND possession_blocks.enumerated_blocks = length_possession_block.enumerated_blocks
    ORDER BY season, gameid, eventid, moment_num
--	LIMIT 500;
