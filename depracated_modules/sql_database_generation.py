# Commands strictly used by me that are used to populate the database (PUT)

import db_connection as connect

def generate_blank_database(database_name='NBA'):
    
    with connect.create_database() as conn:
        
        cursor = conn.cursor()

        cursor.execute(f'DROP DATABASE IF EXISTS {database_name};')
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")

def create_team_table(database_name='NBA'):

    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        #Create the Table
        sql_statement = ''' CREATE TABLE IF NOT EXISTS teams (
        id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(255),
        conference INT)'''

        cursor.execute(sql_statement)

        teams = [['Boston Celtics', 'Brooklyn Nets', 'Toronto Raptors', 'Philadelphia 76ers', 'New York Knicks'],
                 ['Minnesota Timberwolves', 'Oklahoma City Thunder', 'Denver Nuggets', 'Portland Trail Blazers', 'Utah Jazz'],
                 ['Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks'],
                 ['Los Angeles Lakers', 'Los Angeles Clippers', 'Golden State Warriors', 'Phoenix Suns', 'Sacramento Kings'],
                 ['Washington Wizards', 'Atlanta Hawks', 'Orlando Magic', 'Miami Heat', 'Charlotte Hornets'],
                 ['Memphis Grizzlies', 'New Orleans Pelicans', 'Houston Rockets', 'San Antonio Spurs', 'Dallas Mavericks']]
        
        sql_statement = '''INSERT INTO teams (team_name, conference) VALUES (%s,%s)'''

        for i in range(len(teams)):
            for team in teams[i]:
                cursor.execute(sql_statement, (team, i+1))

        conn.commit()

def create_seasons_table(database_name='NBA'):

    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''CREATE TABLE IF NOT EXISTS seasons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        year INT)'''

        cursor.execute(sql_statement)

        conn.commit()

def create_dates_table(database_name='NBA'):

    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''CREATE TABLE IF NOT EXISTS dates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        game_date DATE,
        season INT,
        FOREIGN KEY (season) REFERENCES seasons(id)
        )'''

        cursor.execute(sql_statement)

        conn.commit()

def create_boxscores_table(database_name='NBA'):

    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''CREATE TABLE IF NOT EXISTS boxscores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        home_team INT,
        away_team INT,
        game_date INT,
        url VARCHAR(255),
        FOREIGN KEY (home_team) REFERENCES teams(id),
        FOREIGN KEY (away_team) REFERENCES teams(id),
        FOREIGN KEY (game_date) REFERENCES dates(id)
        )'''

        cursor.execute(sql_statement)

        conn.commit()

def create_team_stats_table(database_name='NBA'):
    
    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''CREATE TABLE IF NOT EXISTS team_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        team INT,
        boxscore INT,
        field_goals INT,
        field_goal_attempts INT,
        three_pointers INT,
        three_point_attempts INT,
        free_throws INT,
        free_throw_attempts INT,
        offensive_rebounds INT,
        defensive_rebounds INT,
        total_rebounds INT,
        assists INT,
        steals INT,
        blocks INT,
        turnovers INT,
        fouls INT,
        points INT,
        FOREIGN KEY (team) REFERENCES teams(id),
        FOREIGN KEY (boxscore) REFERENCES boxscores(id)
        )'''

        cursor.execute(sql_statement)

        conn.commit()

def create_players_table(database_name='NBA'):
    
    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        sql_statment = '''CREATE TABLE IF NOT EXISTS players (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        middle_name VARCHAR(255),
        birthday DATE
        )'''

        cursor.execute(sql_statment)

        conn.commit()

def create_player_stats_table(database_name='NBA'):
    
    with connect.connect_to_database(db=database_name) as conn:
        
        cursor = conn.cursor()

        sql_statement = '''CREATE TABLE IF NOT EXISTS player_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player INT,
        team INT,
        boxscore INT,
        minutes_played INT,
        field_goals INT,
        field_goal_attempts INT,
        three_pointers INT,
        three_point_attempts INT,
        free_throws INT,
        free_throw_attempts INT,
        offensive_rebounds INT,
        defensive_rebounds INT,
        total_rebounds INT,
        assists INT,
        steals INT,
        blocks INT,
        turnovers INT,
        fouls INT,
        points INT,
        FOREIGN KEY (player) REFERENCES players(id),
        FOREIGN KEY (team) REFERENCES teams(id),
        FOREIGN KEY (boxscore) REFERENCES boxscores(id)
        )'''

        cursor.execute(sql_statement)

        conn.commit()

def generate_db(database_name):
    generate_blank_database(database_name)
    create_team_table(database_name)
    create_seasons_table(database_name)
    create_dates_table(database_name)
    create_boxscores_table(database_name)
    create_team_stats_table(database_name)
    create_players_table(database_name)
    create_player_stats_table(database_name)

if __name__ == '__main__':
    generate_db("nba")