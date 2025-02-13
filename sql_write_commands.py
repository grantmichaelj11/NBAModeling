import db_connection as connect
from datetime import datetime

def add_season_to_table(season, database='NBA'):

    with connect.connect_to_database(database) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''SELECT 1 FROM seasons WHERE year = (%s)'''
        cursor.execute(sql_statement, (season,))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO seasons (year) VALUES (%s)', (season,))

        conn.commit()

def add_date_to_table(date, current_season, database='NBA'):

    with connect.connect_to_database(database) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''SELECT 1 FROM dates WHERE game_date = (%s)'''
        cursor.execute(sql_statement, (date,))
        result = cursor.fetchone()

        if not result:
            cursor.execute("SELECT * FROM seasons WHERE year = (%s)", (current_season,))
            season = cursor.fetchone()[0]
            cursor.execute('INSERT INTO dates (game_date, season) VALUES (%s, %s)', (date, season))

        conn.commit()

def retrieve_boxscores(year, month=None, day=None, database='NBA'):

    with connect.connect_to_database(database) as conn:

        cursor = conn.cursor()

        if day is not None and month is not None:
            sql_statement = """
            SELECT 
                boxscores.id,
                boxscores.url
            FROM boxscores
            JOIN dates ON boxscores.game_date = dates.id
            WHERE YEAR(dates.game_date) = '{}'
            AND MONTH(dates.game_date) = '{}'
            AND DAY(dates.game_date) = '{}';
            """.format(year, month, day)

        elif day is None and month is not None:
            sql_statement = """
            SELECT 
                boxscores.id,
                boxscores.url
            FROM boxscores
            JOIN dates ON boxscores.game_date = dates.id
            WHERE YEAR(dates.game_date) = '{}'
            AND MONTH(dates.game_date) = '{}';
            """.format(year, month)

        elif day is None and month is None:
            sql_statement = """
            SELECT 
                boxscores.id,
                boxscores.url
            FROM boxscores
            JOIN dates ON boxscores.game_date = dates.id
            WHERE YEAR(dates.game_date) = '{}';
            """.format(year)

        cursor.execute(sql_statement)
        boxscores = cursor.fetchall()

    return boxscores

def add_boxscore_to_table(date, home_team, away_team, url, database='NBA'):

    with connect.connect_to_database(database) as conn:
        
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM teams WHERE team_name = (%s)", (home_team,))
        home = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM teams WHERE team_name = (%s)", (away_team,))
        away = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM dates WHERE game_date = (%s)", (date,))
        current_date = cursor.fetchone()[0]

        cursor.execute("SELECT 1 FROM boxscores WHERE home_team = %s AND away_team = %s AND game_date = %s", (home, away, current_date))
        result = cursor.fetchone()

        if not result:
            url = 'basketball-reference.com' + url
            cursor.execute('INSERT INTO boxscores (home_team, away_team, game_date, url) VALUES (%s, %s, %s, %s)', (home, away, current_date, url))

            conn.commit()

def retrieve_player_information(first_name, middle_name, last_name, birthday, database='NBA'):

    with connect.connect_to_database(database) as conn:
        
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM players WHERE first_name = %s AND middle_name = %s AND last_name = %s AND birthday = %s", (first_name, middle_name, last_name, birthday))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO players (first_name, middle_name, last_name, birthday) VALUES (%s, %s, %s, %s)', (first_name, middle_name, last_name, birthday))
            conn.commit()

            cursor.execute("SELECT * FROM players WHERE first_name = %s AND middle_name = %s AND last_name = %s AND birthday = %s", (first_name, middle_name, last_name, birthday))
            result = cursor.fetchone()

        return result
        
def add_player_stat_information(player, team, boxscore, minutes_played, field_goals, field_goal_attempts, threes, three_point_attempts,
                                free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds,
                                total_rebounds, assists, steals, blocks, turnovers, personal_fouls, points, database='NBA'):

    with connect.connect_to_database(database) as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM player_stats WHERE player = %s AND team = %s AND boxscore = %s", (player, team, boxscore))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO player_stats (player, team, boxscore, minutes_played, field_goals, field_goal_attempts, three_pointers, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, fouls, points) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (player, team, boxscore, minutes_played, field_goals, field_goal_attempts, threes, three_point_attempts,
                            free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists,
                            steals, blocks, turnovers, personal_fouls, points))
            
            conn.commit()

def retrieve_team_information(team_name, database='NBA'):

    with connect.connect_to_database(database) as conn:
        
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM teams WHERE team_name = %s", (team_name,))

        result = cursor.fetchone()

        return result

def add_team_stat_information(team, boxscore, field_goals, field_goal_attempts, threes, three_point_attempts,
                            free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, 
                            total_rebounds, assists, steals, blocks, turnovers, personal_fouls, points, database='NBA'):
    
    with connect.connect_to_database(database) as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM team_stats WHERE team = %s AND boxscore = %s", (team, boxscore))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO team_stats (team, boxscore, field_goals, field_goal_attempts, three_pointers, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, fouls, points) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (team, boxscore, field_goals, field_goal_attempts, threes, three_point_attempts,
                                free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists,
                                steals, blocks, turnovers, personal_fouls, points))
            
            conn.commit()

