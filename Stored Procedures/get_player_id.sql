DELIMITER //

CREATE PROCEDURE get_player_id(
    IN first_name VARCHAR(255), 
    IN last_name VARCHAR(255), 
    IN middle_name VARCHAR(255), 
    IN birthday DATE
)
BEGIN
    IF middle_name IS NULL THEN
        SELECT 
            CONCAT(players.first_name, 
                   CASE 
                       WHEN players.middle_name IS NOT NULL AND players.middle_name != '' THEN CONCAT(' ', players.middle_name) 
                       ELSE '' 
                   END, 
                   ' ', players.last_name) AS player_name,
		players.id
        FROM players
        WHERE (players.first_name = first_name OR players.middle_name LIKE CONCAT(first_name, '%')) 
          AND players.last_name LIKE CONCAT(last_name, '%') 
          AND (birthday IS NULL OR players.birthday = birthday);
    END IF;
    
    IF middle_name IS NOT NULL THEN
        SELECT 
            CONCAT(players.first_name, 
                   CASE 
                       WHEN players.middle_name IS NOT NULL AND players.middle_name != '' THEN CONCAT(' ', players.middle_name) 
                       ELSE '' 
                   END, 
                   ' ', players.last_name) AS player_name,
		players.id
        FROM players
        WHERE (players.first_name = first_name OR players.middle_name LIKE CONCAT(first_name, '%')) 
          AND players.last_name LIKE CONCAT(last_name, '%') 
          AND players.middle_name = middle_name
          AND (birthday IS NULL OR players.birthday = birthday);
    END IF;
END //

DELIMITER ;