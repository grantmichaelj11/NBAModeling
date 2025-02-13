 DELIMITER //
CREATE PROCEDURE get_team_stats_for_date(IN team_name VARCHAR(255), IN game_date date)
BEGIN
	SELECT
		dates.game_date AS game_date,
		seasons.year AS season,
		currentTeam.team_name AS team,
		team.field_goals AS field_goals,
		team.field_goal_attempts AS field_goal_attempts,
		team.three_pointers AS three_pointers,
		team.three_point_attempts AS three_point_attempts,
		team.free_throws AS free_throws,
		team.free_throw_attempts AS free_throw_attempts,
		team.offensive_rebounds AS offensive_rebounds,
		team.defensive_rebounds AS defensive_rebounds,
		team.total_rebounds AS total_rebounds,
		team.assists AS assists,
		team.steals AS steals,
		team.blocks AS blocks,
		team.turnovers AS turnovers,
		team.fouls as fouls,
		team.points as points,
		opponentTeam.team_name AS opponent,
		opponent.field_goals AS opponent_field_goals,
		opponent.field_goal_attempts AS opponent_field_goal_attempts,
		opponent.three_pointers AS opponent_three_pointers,
		opponent.three_point_attempts AS opponent_three_point_attempts,
		opponent.free_throws AS opponent_free_throws,
		opponent.free_throw_attempts AS opponent_free_throw_attempts,
		opponent.offensive_rebounds AS opponent_offensive_rebounds,
		opponent.defensive_rebounds AS opponent_defensive_rebounds,
		opponent.total_rebounds AS opponent_total_rebounds,
		opponent.assists AS opponent_assists,
		opponent.steals AS opponent_steals,
		opponent.blocks AS opponent_blocks,
		opponent.turnovers AS opponent_turnovers,
		opponent.fouls as opponent_fouls,
		opponent.points as opponent_points
	FROM team_stats AS team
	JOIN team_stats AS opponent ON team.boxscore = opponent.boxscore AND team.team != opponent.team
	LEFT JOIN teams AS currentTeam ON currentTeam.id = team.team
	LEFT JOIN teams AS opponentTeam ON opponentTeam.id = opponent.team
	LEFT JOIN boxscores ON boxscores.id=team.boxscore
	LEFT JOIN dates ON dates.id=boxscores.game_date
	LEFT JOIN seasons ON seasons.id=dates.season
	WHERE currentTeam.team_name=team_name AND dates.game_date=game_date;
    
END //

DELIMITER ;
