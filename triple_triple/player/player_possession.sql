/* eventually this will require playerid list as input */

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
, closest_to_ball AS (
    SELECT 
        ball_dist.season
      , ball_dist.gameid
      , ball_dist.eventid
      , ball_dist.moment_num
      , ball_dist.teamid
      , ball_dist.playerid
      , ball_dist.distance_from_ball
      , ROW_NUMBER() OVER (
          PARTITION BY gameid, eventid, moment_num 
          ORDER BY distance_from_ball)  AS closest_to_ball_rank
    FROM ball_dist
    WHERE playerid != -1 -- remove the ball since some moments don't have it and it affects the row number
)
SELECT 
      ball_dist.*
    , closest_to_ball.closest_to_ball_rank
FROM ball_dist
  LEFT JOIN closest_to_ball
    ON ball_dist.season = closest_to_ball.season
    AND ball_dist.gameid = closest_to_ball.gameid
    AND ball_dist.eventid = closest_to_ball.eventid
    AND ball_dist.moment_num = closest_to_ball.moment_num
    AND ball_dist.teamid = closest_to_ball.teamid
    AND ball_dist.playerid = closest_to_ball.playerid