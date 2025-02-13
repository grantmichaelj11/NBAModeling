DELIMITER //
CREATE PROCEDURE get_player_model(input_id int)
BEGIN
	SELECT
		id,
		player_id,
		creation_date,
        model_file,
        skewness,
        mean,
        scale
	FROM models
	WHERE player_id = input_id;
    
END //

DELIMITER ;
