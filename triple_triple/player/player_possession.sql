/* eventually this will require the following variables:
- playerid list 
- has_ball_distances input 
- length of consecutive closest_to_ball frames to qualify for possession 
*/

/* this query scans through everything (to find the games for specific players) 
and costs a lot of $$ 
For now, to test hte logic, in the cte relevant_gameid, 
WHERE clause is for specific game, not players
*/


WITH relevant_gameid AS (
    SELECT DISTINCT gameid
    FROM nba.playerinfo
    -- WHERE playerid IN (202714, 201952)
    WHERE gameid = '0021500128'
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
      , POWER(x_coordinate - x_coordinate_ball, 2) +
        POWER(y_coordinate - y_coordinate_ball, 2)
                                        AS distance_from_ball_sq
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
      , ball_dist.distance_from_ball_sq
      , ROW_NUMBER() OVER (
          PARTITION BY season, gameid, eventid, moment_num 
          ORDER BY distance_from_ball_sq)  AS closest_to_ball_rank   
    FROM ball_dist
    WHERE playerid != -1 -- remove the ball since some moments don't have it
)
, closest_to_ball AS (
    SELECT
        season
      , gameid
      , eventid
      , moment_num
      , teamid
      , playerid
      , closest_to_ball_rank
    FROM rank_ball_dist
    WHERE closest_to_ball_rank = 1 AND distance_from_ball_sq <= 4 -- distance squared. input as variable
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
	FROM closest_to_ball
)
/* this enumerates the blocks */
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
      , ball_dist.distance_from_ball_sq
	  , length_possession_block.possession_length
    --   , CASE WHEN length_possession_block.possession_length >= 25 THEN 1 ELSE 0 -- make 25 a variable
    --     END                             AS has_ball          
	FROM ball_dist
	  LEFT JOIN rank_ball_dist -- only get players, not ball
        ON  ball_dist.season = rank_ball_dist.season
        AND ball_dist.gameid = rank_ball_dist.gameid
        AND ball_dist.eventid = rank_ball_dist.eventid
        AND ball_dist.moment_num = rank_ball_dist.moment_num
        AND ball_dist.playerid = rank_ball_dist.playerid
       INNER JOIN closest_to_ball -- so that we only get players where closest_to_ball_rank = 1
        ON  closest_to_ball.season = rank_ball_dist.season
        AND closest_to_ball.gameid = rank_ball_dist.gameid
        AND closest_to_ball.eventid = rank_ball_dist.eventid
        AND closest_to_ball.moment_num = rank_ball_dist.moment_num
        AND closest_to_ball.playerid = rank_ball_dist.playerid
        AND closest_to_ball.closest_to_ball_rank = rank_ball_dist.closest_to_ball_rank
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
--	LIMIT 500;
