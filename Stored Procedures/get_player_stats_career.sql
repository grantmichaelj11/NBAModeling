 DELIMITER //

CREATE PROCEDURE get_player_stats_career(IN first_name VARCHAR(255), IN last_name VARCHAR(255), IN middle_name VARCHAR(255))
BEGIN
    IF middle_name IS NULL THEN
		SELECT 
        CONCAT(players.first_name, 
               CASE 
                   WHEN players.middle_name IS NOT NULL AND players.middle_name != '' THEN CONCAT(' ', players.middle_name) 
                   ELSE '' 
               END, 
               ' ', players.last_name) AS player_name,
        AVG(player_stats.minutes_played) as minutes_played,
        AVG(player_stats.field_goals) as field_goals,
        AVG(player_stats.field_goal_attempts) as field_goal_attempts,
        AVG(player_stats.three_pointers) as three_pointers,
        AVG(player_stats.three_point_attempts) as three_point_attempts,
        AVG(player_stats.free_throws) as free_throws,
        AVG(player_stats.free_throw_attempts) as free_throw_attempts,
        AVG(player_stats.offensive_rebounds) as offensive_rebounds,
        AVG(player_stats.defensive_rebounds) as defensive_rebounds,
        AVG(player_stats.total_rebounds) as total_rebounds,
        AVG(player_stats.assists) as assists,
        AVG(player_stats.steals) as steals,
        AVG(player_stats.blocks) as blocks,
        AVG(player_stats.turnovers) as turnovers,
        AVG(player_stats.fouls) as fouls,
        AVG(player_stats.points) as points
        FROM player_stats
        LEFT JOIN players ON players.id=player_stats.player
        LEFT JOIN teams ON teams.id=player_stats.team
        LEFT JOIN boxscores ON boxscores.id=player_stats.boxscore
        LEFT JOIN dates ON dates.id = boxscores.game_date
        LEFT JOIN seasons ON seasons.id = dates.season
        LEFT JOIN teams AS home_teams ON home_teams.id = boxscores.home_team
        LEFT JOIN teams AS away_teams ON away_teams.id = boxscores.away_team
        WHERE (players.first_name=first_name OR players.middle_name LIKE CONCAT(first_name, '%')) AND players.last_name LIKE CONCAT(last_name, '%') AND player_stats.minutes_played != 0
        GROUP BY players.first_name, players.middle_name, players.last_name;
    END IF;
    
    IF middle_name is NOT NULL THEN
		SELECT 
        CONCAT(players.first_name, 
               CASE 
                   WHEN players.middle_name IS NOT NULL AND players.middle_name != '' THEN CONCAT(' ', players.middle_name) 
                   ELSE '' 
               END, 
               ' ', players.last_name) AS player_name,
		AVG(player_stats.minutes_played) as minutes_played,
        AVG(player_stats.field_goals) as field_goals,
        AVG(player_stats.field_goal_attempts) as field_goal_attempts,
        AVG(player_stats.three_pointers) as three_pointers,
        AVG(player_stats.three_point_attempts) as three_point_attempts,
        AVG(player_stats.free_throws) as free_throws,
        AVG(player_stats.free_throw_attempts) as free_throw_attempts,
        AVG(player_stats.offensive_rebounds) as offensive_rebounds,
        AVG(player_stats.defensive_rebounds) as defensive_rebounds,
        AVG(player_stats.total_rebounds) as total_rebounds,
        AVG(player_stats.assists) as assists,
        AVG(player_stats.steals) as steals,
        AVG(player_stats.blocks) as blocks,
        AVG(player_stats.turnovers) as turnovers,
        AVG(player_stats.fouls) as fouls,
        AVG(player_stats.points) as points
        FROM player_stats
        LEFT JOIN players ON players.id=player_stats.player
        LEFT JOIN teams ON teams.id=player_stats.team
        LEFT JOIN boxscores ON boxscores.id=player_stats.boxscore
        LEFT JOIN dates ON dates.id = boxscores.game_date
        LEFT JOIN seasons ON seasons.id = dates.season
        LEFT JOIN teams AS home_teams ON home_teams.id = boxscores.home_team
        LEFT JOIN teams AS away_teams ON away_teams.id = boxscores.away_team
        WHERE (players.first_name=first_name OR players.middle_name LIKE CONCAT(first_name, '%')) AND players.last_name LIKE CONCAT(last_name, '%') AND players.middle_name=middle_name AND player_stats.minutes_played != 0
        GROUP BY players.first_name, players.middle_name, players.last_name;
    END IF;
    
END //

DELIMITER ;