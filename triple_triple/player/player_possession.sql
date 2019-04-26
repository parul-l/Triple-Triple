/* eventually this will require playerid list and has_ball_distanceas input */

WITH relevant_gameid AS (
    SELECT DISTINCT gameid
    FROM nba.playerinfo
    WHERE playerid IN (202714, 201952)
)
, ball_info AS (
    SELECT 
        nba.gameposition.gameid
	  , nba.gameposition.eventid
      , nba.gameposition.moment_num
      , nba.gameposition.x_coordinate
      , nba.gameposition.y_coordinate
    FROM nba.gameposition
      INNER JOIN relevant_gameid 
        ON nba.gameposition.gameid = relevant_gameid.gameid
    WHERE playerid = -1
)
, position_ball AS (
    SELECT 
        nba.gameposition.*
      , ball_info.x_coordinate          AS x_coordinate_ball
      , ball_info.y_coordinate          AS y_coordinate_ball
    FROM nba.gameposition
      INNER JOIN relevant_gameid 
        ON nba.gameposition.gameid = relevant_gameid.gameid      
      LEFT JOIN ball_info
        ON nba.gameposition.gameid = ball_info.gameid
        AND nba.gameposition.eventid = ball_info.eventid
        AND nba.gameposition.moment_num = ball_info.moment_num
) 
, ball_dist AS (
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
      , SQRT(
          POWER(x_coordinate - x_coordinate_ball, 2) +
          POWER(y_coordinate - y_coordinate_ball, 2)
        )
                                        AS distance_from_ball
    FROM position_ball
)
, rank_ball_dist AS (
    SELECT 
        ball_dist.season
      , ball_dist.gameid
      , ball_dist.eventid
      , ball_dist.moment_num
      , ball_dist.teamid
      , ball_dist.playerid
      , ball_dist.distance_from_ball
      , ROW_NUMBER() OVER (
          PARTITION BY season, gameid, eventid, moment_num 
          ORDER BY distance_from_ball)  AS closest_to_ball_rank   
--   , CASE WHEN 
--       ROW_NUMBER() OVER (
--       PARTITION BY season, gameid, eventid, moment_num ORDER BY distance_from_ball) = 1 
--       AND distance_from_ball <= 2
--     THEN 1 ELSE 0 END                   AS is_closest_to_ball_within_threshold
    FROM ball_dist
    WHERE playerid != -1 -- remove the ball since some moments don't have it and it affects the row number
)
, closest_count AS (
    SELECT
        season
      , gameid
      , eventid
      , moment_num
      , teamid
      , playerid
      , closest_to_ball_rank
    FROM rank_ball_dist
    WHERE closest_to_ball_rank = 1 AND distance_from_ball <= 2
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
	FROM closest_count
)
, possession_blocks AS (
	SELECT 
		season
	  , gameid
	  , eventid
	  , moment_num
	  , playerid
	  , SUM(is_different_player_is_closest) OVER (ORDER BY season, gameid, eventid, moment_num) AS enumerated_blocks
	FROM shifted_closest_player
)
, length_possession_block AS (
	SELECT
	  playerid
	  , enumerated_blocks
	  , COUNT(*)	AS possession_length
	FROM possession_blocks
	GROUP BY playerid, enumerated_blocks	
)     
	SELECT      
        ball_dist.season
      , ball_dist.gameid
      , ball_dist.eventid
      , ball_dist.moment_num
      , ball_dist.timestamp_dts
      , ball_dist.timestamp_utc
      , ball_dist.period
      , ball_dist.periodclock
      , ball_dist.shotclock
      , ball_dist.teamid
      , ball_dist.playerid
      , ball_dist.x_coordinate
      , ball_dist.y_coordinate
      , ball_dist.z_coordinate
      , ball_dist.distance_from_ball
      , possession_blocks.enumerated_blocks
	  , length_possession_block.possession_length
	FROM ball_dist
	  LEFT JOIN rank_ball_dist 
        ON  ball_dist.season = rank_ball_dist.season
        AND ball_dist.gameid = rank_ball_dist.gameid
        AND ball_dist.eventid = rank_ball_dist.eventid
        AND ball_dist.moment_num = rank_ball_dist.moment_num
        AND ball_dist.playerid = rank_ball_dist.playerid
       INNER JOIN closest_count -- so that we only get players with possession (closest_to_ball_rank = 1)
        ON  closest_count.season = rank_ball_dist.season
        AND closest_count.gameid = rank_ball_dist.gameid
        AND closest_count.eventid = rank_ball_dist.eventid
        AND closest_count.moment_num = rank_ball_dist.moment_num
        AND closest_count.playerid = rank_ball_dist.playerid
        AND closest_count.closest_to_ball_rank = rank_ball_dist.closest_to_ball_rank
      LEFT JOIN possession_blocks
        ON  possession_blocks.season = rank_ball_dist.season
        AND possession_blocks.gameid = rank_ball_dist.gameid
        AND possession_blocks.eventid = rank_ball_dist.eventid
        AND possession_blocks.moment_num = rank_ball_dist.moment_num
        AND possession_blocks.playerid = rank_ball_dist.playerid
      LEFT JOIN length_possession_block
        ON  possession_blocks.playerid = length_possession_block.playerid
        AND possession_blocks.enumerated_blocks = length_possession_block.enumerated_blocks
        ORDER BY season, gameid, eventid, moment_num
	LIMIT 50;
