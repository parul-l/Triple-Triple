/*
This query combines player possession with player actions to determine 
the position of each action. Assumptions to determine possession 
are made in creating the vw_poss_tmp view.

For each action, we find the eventid, moment_num is the possesion view that
has the closest period_clock to the action's period_tim.

We have not addressed:
- where the closest eventid, moment_num has a "large" |period_time - periodclock|
- where two actions at two different times result in the same possession block
*/
CREATE VIEW nba.vw_action_region AS
    WITH poss_action AS (
        SELECT
            player_actions.season
            , player_actions.gameid
            , player_actions.eventnum
            , player_actions.period
            , player_actions.period_time
            , player_actions.eventmsgtype
            , player_actions.eventmsgactiontype
            , player_actions.event_action
            , player_actions.event_subaction
            , player_actions.description
            , player_actions.playerid
            , player_actions.playername
            , player_actions.is_home
            , vw_poss_tmp.eventid
            , vw_poss_tmp.moment_num
            , vw_poss_tmp.periodclock
            , vw_poss_tmp.court_region
            , vw_poss_tmp.possession_length
            , vw_poss_tmp.enumerated_blocks
            , ABS(player_actions.period_time - vw_poss_tmp.periodclock) AS diff_possclock_actionclock
        FROM nba.player_actions
        LEFT JOIN nba.vw_poss_tmp
        ON   player_actions.season = vw_poss_tmp.season
        AND  player_actions.gameid = vw_poss_tmp.gameid
        AND  player_actions.playerid = vw_poss_tmp.playerid
        AND  player_actions.period = vw_poss_tmp.period
        WHERE player_actions.gameid IN {0}
        AND   player_actions.playerid IN {1}
        AND   player_actions.eventmsgtype NOT IN (3, 6, 8) -- 3 = freethrow, 6 = foul, 8 = substitution 
        AND   vw_poss_tmp.gameid IN {0}
        AND   vw_poss_tmp.playerid IN {1}
    )
    , dist_order AS (
        SELECT 
        season
        , gameid
        , playerid
        , eventnum
        , eventid
        , moment_num 
        , ROW_NUMBER() OVER (PARTITION BY season, gameid, playerid, eventnum ORDER BY diff_possclock_actionclock, eventid, moment_num) AS distrank
        FROM poss_action
    )
    SELECT
        poss_action.eventnum 
        , poss_action.eventid
        , poss_action.moment_num
        , poss_action.period
        , poss_action.eventmsgtype
        , poss_action.eventmsgactiontype
        , poss_action.event_action
        , poss_action.event_subaction
        , poss_action.description
        , poss_action.playerid
        , poss_action.playername
        , poss_action.is_home
        , poss_action.court_region
        , poss_action.diff_possclock_actionclock
        , poss_action.possession_length
        , poss_action.enumerated_blocks
        , poss_action.season
        , poss_action.gameid
    FROM poss_action
    INNER JOIN dist_order
        ON  poss_action.season = dist_order.season
        AND poss_action.gameid = dist_order.gameid
        AND poss_action.playerid = dist_order.playerid
        AND poss_action.eventnum = dist_order.eventnum
        AND poss_action.eventid = dist_order.eventid
        AND poss_action.moment_num = dist_order.moment_num
        WHERE dist_order.distrank = 1
	