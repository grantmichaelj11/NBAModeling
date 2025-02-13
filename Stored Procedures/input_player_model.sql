DELIMITER //
CREATE PROCEDURE input_player_model(input_player_id int, input_model_file longblob, input_skewness DECIMAL(9,6), input_mean DECIMAL(9,6), input_scale DECIMAL(9,6))
BEGIN

	DECLARE last_date INT;
    SELECT id INTO last_date
    FROM dates
    ORDER BY id DESC
    LIMIT 1;
    
    IF NOT EXISTS (SELECT 1 FROM models WHERE player_id = input_player_id) THEN
		INSERT INTO models (player_id, creation_date, model_file, skewness, mean, scale)
		VALUES (input_player_id, last_date, input_model_file, input_skewness, input_mean, input_scale);
    END IF;
    
END //

DELIMITER ;
