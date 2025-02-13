DELIMITER //

CREATE PROCEDURE get_all_teams()
BEGIN
	SELECT
		team_name as team,
        CASE conference
			WHEN 1 THEN 'Atlantic'
            WHEN 2 THEN 'Northwest'
            WHEN 3 THEN 'Central'
            WHEN 4 THEN 'Pacific'
            WHEN 5 THEN 'Southeast'
            WHEN 6 THEN 'Southwest'
		END as division
	FROM teams;
END //

DELIMITER ;