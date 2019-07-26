CREATE VIEW {} AS 
    SELECT 
          gameposition.season
        , gameposition.gameid
        , gameposition.eventid
        , gameposition.moment_num
        , gameposition.period
        , gameposition.periodclock
        , gameposition.shotclock
        , team_shooting_side.shooting_side
        , gameposition.teamid
        , gameposition.playerid
        , gameposition.x_coordinate
        , gameposition.y_coordinate
        , gameposition.z_coordinate
        , CASE WHEN (shooting_side = 'left' 
                AND  x_coordinate >= 47 AND x_coordinate <= 94 AND
                    y_coordinate >= 0 AND y_coordinate <= 50)
                OR  (shooting_side = 'right' 
                AND  x_coordinate >= 0 AND x_coordinate <= 47 AND
                    y_coordinate >= 0 AND y_coordinate <= 50)
                THEN 'backcourt' 
            WHEN (shooting_side = 'left'
                AND (x_coordinate >= 0 AND x_coordinate <= 14 AND
                    ((y_coordinate >=0 AND y_coordinate <= 3) OR 
                    (y_coordinate >=47 AND y_coordinate <= 50)))
                OR  (x_coordinate >= 14 AND x_coordinate < 47 AND 
                    (POWER(x_coordinate - 5.25, 2) + POWER(y_coordinate - 25, 2) > POWER(23.75, 2))))
                OR  (shooting_side = 'right'
                AND (x_coordinate >= 80 AND x_coordinate <= 94 AND
                    ((y_coordinate >=0 AND y_coordinate <= 3) OR 
                    (y_coordinate >=47 AND y_coordinate <= 50)))
                OR  (x_coordinate > 47 AND x_coordinate <= 80 AND 
                    (POWER(x_coordinate - 88.75, 2) + POWER(y_coordinate - 25, 2) > POWER(23.75, 2))))
                THEN 'perimeter'
            WHEN (shooting_side = 'left'
                AND (x_coordinate >= 0 AND x_coordinate <= 14 AND
                    ((y_coordinate >=3 AND y_coordinate <= 19) OR 
                    (y_coordinate >=31 AND y_coordinate <= 47)))
                OR  ((y_coordinate <= 19 OR y_coordinate >=31) AND
                    x_coordinate >= 14 AND x_coordinate <= 19 AND
                    POWER(x_coordinate - 5.25, 2) + POWER(y_coordinate - 25, 2) <= POWER(23.75, 2))
                OR  (x_coordinate >= 19 AND x_coordinate <= 25 AND
                    POWER(x_coordinate - 5.25, 2) + POWER(y_coordinate - 25, 2) <= POWER(23.75, 2) AND
                    POWER(x_coordinate - 19, 2) + POWER(y_coordinate - 25, 2) >= POWER(6, 2))
                OR  (x_coordinate >= 25 AND x_coordinate <= 29 AND
                    POWER(x_coordinate - 5.25, 2) + POWER(y_coordinate - 25, 2) <= POWER(23.75, 2)))
                OR (shooting_side = 'right'
                AND (x_coordinate >= 80 AND x_coordinate <= 94 AND
                    ((y_coordinate >=3 AND y_coordinate <= 19) OR 
                    (y_coordinate >=31 AND y_coordinate <= 47)))
                OR  ((y_coordinate <= 19 OR y_coordinate >=31) AND
                    x_coordinate >= 75 AND x_coordinate <= 80 AND
                    POWER(x_coordinate - 88.75, 2) + POWER(y_coordinate - 25, 2) <= POWER(23.75, 2))
                OR  (x_coordinate >= 69 AND x_coordinate <= 75 AND
                    POWER(x_coordinate - 88.75, 2) + POWER(y_coordinate - 25, 2) <= POWER(23.75, 2) AND
                    POWER(x_coordinate - 75, 2) + POWER(y_coordinate - 25, 2) >= POWER(6, 2))
                OR  (x_coordinate >= 65 AND x_coordinate <= 69 AND
                    POWER(x_coordinate - 88.75, 2) + POWER(y_coordinate - 25, 2) <= POWER(23.75, 2)))        
                THEN 'midrange'
            WHEN (shooting_side = 'left'
                AND (x_coordinate >= 19 AND x_coordinate <= 25 AND
                    POWER(x_coordinate - 19, 2) + POWER(y_coordinate - 25, 2) <= POWER(6, 2)))
                OR  (shooting_side = 'right'
                AND (x_coordinate >= 69 AND x_coordinate <= 75 AND
                    POWER(x_coordinate - 75, 2) + POWER(y_coordinate - 25, 2) <= POWER(6, 2)))
                THEN 'key'
            WHEN (shooting_side = 'left'
                AND x_coordinate >=0 AND x_coordinate <= 19
                AND y_coordinate >= 19 AND y_coordinate <= 31)
                OR (shooting_side = 'right'
                AND x_coordinate >=75 AND x_coordinate <= 95
                AND y_coordinate >= 19 AND y_coordinate <= 31)
                THEN 'paint'
            WHEN x_coordinate <= 0 OR x_coordinate >= 94
                OR  y_coordinate <= 0 OR y_coordinate >= 50
                THEN 'out_of_bounds' 
        ELSE NULL END                      AS "court_region"
    FROM nba.gameposition
      INNER JOIN nba.team_shooting_side USING (teamid, period)
    WHERE nba.gameposition.gameid IN {}
      AND nba.team_shooting_side.gameid IN {}
      AND nba.gameposition.playerid IN {}
