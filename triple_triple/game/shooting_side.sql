-- gameid should be a variable

WITH first_bucket AS (
	SELECT 
		  gameid
		, period
		, player1_team_id					AS teamid
		, CAST(SUBSTRING(pctimestring, 1, STRPOS(pctimestring, ':') - 1) AS TINYINT) * 60 +
	      CAST(SUBSTRING(pctimestring, STRPOS(pctimestring, ':') + 1, LENGTH(pctimestring)) AS TINYINT) 
                                            AS periodclock
	FROM nba.playbyplay
	WHERE gameid = '0021500128'
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
    SELECT
          gameid
        , period
        , teamid
        , MAX(periodclock)	                AS periodclock
        , MAX(shotclock)	                AS shotclock
    FROM nba.gameposition
    WHERE gameid = '0021500128' AND teamid != -1 
    GROUP BY gameid, period, teamid
    ORDER BY gameid, period, teamid
)
    SELECT
        gamelog.season
      , gamelog.gameid
      , gamelog.game_date
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
        END                       	AS shooting_side
      , CURRENT_TIMESTAMP           AS lastupdate_DTS
    FROM team_period
      LEFT JOIN first_shot_shooting_side
        ON  team_period.gameid = first_shot_shooting_side.gameid
      --  AND team_period.teamid = first_shot_shooting_side.teamid (only join on gameid so that shooting side/teamid not null when no match)
      LEFT JOIN nba.gamelog
        ON  gamelog.gameid = team_period.gameid
        AND gamelog.team_id = team_period.teamid   