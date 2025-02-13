 DELIMITER //

CREATE PROCEDURE get_player_stats_for_season(IN first_name VARCHAR(255), IN last_name VARCHAR(255), IN middle_name VARCHAR(255),  IN season_year INT)
BEGIN
    IF middle_name IS NULL THEN
		SELECT 
        CONCAT(players.first_name, 
               CASE 
                   WHEN players.middle_name IS NOT NULL AND players.middle_name != '' THEN CONCAT(' ', players.middle_name) 
                   ELSE '' 
               END, 
               ' ', players.last_name) AS player_name,
        seasons.year as season,
        dates.game_date,
        teams.team_name as player_team,
        opponent_teams.team_name as opponent_team,
        player_stats.minutes_played,
        player_stats.field_goals,
        player_stats.field_goal_attempts,
        player_stats.three_pointers,
        player_stats.three_point_attempts,
        player_stats.free_throws,
        player_stats.free_throw_attempts,
        player_stats.offensive_rebounds,
        player_stats.defensive_rebounds,
        player_stats.total_rebounds,
        player_stats.assists,
        player_stats.steals,
        player_stats.blocks,
        player_stats.turnovers,
        player_stats.fouls,
        player_stats.points
        FROM player_stats
        LEFT JOIN players ON players.id=player_stats.player
        LEFT JOIN teams ON teams.id=player_stats.team
        LEFT JOIN boxscores ON boxscores.id=player_stats.boxscore
        LEFT JOIN dates ON dates.id = boxscores.game_date
        LEFT JOIN seasons ON seasons.id = dates.season
        LEFT JOIN teams AS home_teams ON home_teams.id = boxscores.home_team
        LEFT JOIN teams AS away_teams ON away_teams.id = boxscores.away_team
        LEFT JOIN teams AS opponent_teams ON (
			CASE
				WHEN player_stats.team = boxscores.home_team THEN boxscores.away_team
                WHEN player_stats.team = boxscores.away_team THEN boxscores.home_team
			END = opponent_teams.id
        )
        WHERE (players.first_name=first_name OR players.middle_name LIKE CONCAT(first_name, '%')) AND players.last_name LIKE CONCAT(last_name, '%') AND seasons.year=season_year AND player_stats.minutes_played != 0
		ORDER BY dates.game_date;
    END 
IF;
    
    IF middle_name is NOT NULL THEN
		SELECT 
        CONCAT(players.first_name, 
               CASE 
                   WHEN players.middle_name IS NOT NULL AND players.middle_name != '' THEN CONCAT(' ', players.middle_name) 
                   ELSE '' 
               END, 
               ' ', players.last_name) AS player_name,
        seasons.year as season,
        dates.game_date,
        teams.team_name as player_team,
        opponent_teams.team_name as opponent_team,
        player_stats.minutes_played,
        player_stats.field_goals,
        player_stats.field_goal_attempts,
        player_stats.three_pointers,
        player_stats.three_point_attempts,
        player_stats.free_throws,
        player_stats.free_throw_attempts,
        player_stats.offensive_rebounds,
        player_stats.defensive_rebounds,
        player_stats.total_rebounds,
        player_stats.assists,
        player_stats.steals,
        player_stats.blocks,
        player_stats.turnovers,
        player_stats.fouls,
        player_stats.points
        FROM player_stats
        LEFT JOIN players ON players.id=player_stats.player
        LEFT JOIN teams ON teams.id=player_stats.team
        LEFT JOIN boxscores ON boxscores.id=player_stats.boxscore
        LEFT JOIN dates ON dates.id = boxscores.game_date
        LEFT JOIN seasons ON seasons.id = dates.season
        LEFT JOIN teams AS home_teams ON home_teams.id = boxscores.home_team
        LEFT JOIN teams AS away_teams ON away_teams.id = boxscores.away_team
        LEFT JOIN teams AS opponent_teams ON (
			CASE
				WHEN player_stats.team = boxscores.home_team THEN boxscores.away_team
                WHEN player_stats.team = boxscores.away_team THEN boxscores.home_team
			END = opponent_teams.id
        )
        WHERE (players.first_name=first_name OR players.middle_name LIKE CONCAT(first_name, '%')) AND players.last_name LIKE CONCAT(last_name, '%') AND players.middle_name=middle_name AND seasons.year=season_year AND player_stats.minutes_played != 0
        ORDER BY dates.game_date;
    END IF;
    
END //

DELIMITER ;

