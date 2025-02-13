import sql_write_commands as sql
import db_connection as connect
import sqlite3 as lite
import mysql.connector

#Migrate the data from SQLite3 to the new MySQL DB
#Perhaps a select * in sqllite three and then iterating by row?
#Best to go in order given here as it will handle dependencies

def migrate_seasons():
    #Get all rows for seasons
    with lite.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM seasons')
        old_data = cursor.fetchall()

        #Update this to new database
        for data in old_data:
            sql.add_season_to_table(data[1])

def migrate_dates():
    with lite.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM dates')
        old_data = cursor.fetchall()

        for data in old_data:
            #Get season id
            cursor.execute(f'SELECT * FROM seasons WHERE id = {data[2]}')
            season_year = cursor.fetchone()[1]
            sql.add_date_to_table(data[1], season_year)

def migrate_boxscores():
    with lite.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM boxscores')
        old_data = cursor.fetchall()

        with connect.connect_to_database() as new_conn:
            new_cursor = new_conn.cursor()
            
            for data in old_data:
                new_cursor.execute('INSERT INTO boxscores (home_team, away_team, game_date, url) VALUES (%s, %s, %s, %s)',(data[1], data[2], data[3], data[4]))

            new_conn.commit()
            
def migrate_team_stats():
    with lite.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM team_stats')
        old_data = cursor.fetchall()

        with connect.connect_to_database() as new_conn:
            new_cursor = new_conn.cursor()
            
            for data in old_data:
                new_cursor.execute('INSERT INTO team_stats (team, boxscore, field_goals, field_goal_attempts, three_pointers, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, fouls, points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                   (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17]))

            new_conn.commit()

def migrate_players():
    with lite.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM players')
        old_data = cursor.fetchall()

        with connect.connect_to_database() as new_conn:
            for data in old_data:
                print(data)
                new_cursor = new_conn.cursor()  
                new_cursor.execute("SELECT * FROM players WHERE first_name = %s AND middle_name = %s AND last_name = %s AND birthday = %s", (data[1], data[4], data[2], data[3]))
                result = new_cursor.fetchone()

                if not result:
                    new_cursor.execute('INSERT INTO players (id, first_name, middle_name, last_name, birthday) VALUES (%s, %s, %s, %s, %s)', (data[0], data[1], data[4], data[2], data[3]))
                    new_conn.commit()


def migrate_player_stats():
    with lite.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM player_stats')
        old_data = cursor.fetchall()

        with connect.connect_to_database() as new_conn:
            new_cursor = new_conn.cursor()
            
            for data in old_data:
                try:
                    new_cursor.execute('INSERT INTO player_stats (id, player, team, boxscore, minutes_played, field_goals, field_goal_attempts, three_pointers, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, fouls, points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19]))
                
                    new_conn.commit()
                except mysql.connector.errors.IntegrityError:
                    print(data)
                    break
            

if __name__ == '__main__':
    migrate_seasons()
    migrate_dates()
    migrate_boxscores()
    migrate_team_stats()
    migrate_players()
    migrate_player_stats()