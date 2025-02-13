import sqlite3 as sql
import os
import pandas as pd
import numpy as np
from datetime import datetime, date
import time


########### QUERIES FOR ADDING TO DATABASE ######################
def generate_blank_nba_database(database_name):
    #Remove database if it exists
    if os.path.exists(database_name):
        os.remove(database_name)
    
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        # Create Teams Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       team_name TEXT,
                       conference INTEGER)''')

        teams = [['Boston Celtics', 'Brooklyn Nets', 'Toronto Raptors', 'Philadelphia 76ers', 'New York Knicks'],
                 ['Minnesota Timberwolves', 'Oklahoma City Thunder', 'Denver Nuggets', 'Portland Trail Blazers', 'Utah Jazz'],
                 ['Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks'],
                 ['Los Angeles Lakers', 'Los Angeles Clippers', 'Golden State Warriors', 'Phoenix Suns', 'Sacramento Kings'],
                 ['Washington Wizards', 'Atlanta Hawks', 'Orlando Magic', 'Miami Heat', 'Charlotte Hornets'],
                 ['Memphis Grizzlies', 'New Orleans Pelicans', 'Houston Rockets', 'San Antonio Spurs', 'Dallas Mavericks']]

        for i in range(len(teams)):
            for team in teams[i]:
                cursor.execute('''INSERT INTO teams
                               (team_name, conference)
                               VALUES (?, ?)''',
                               (team, i+1))
                

        # Create Seasons Tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS seasons (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       year INTEGER
        )''')

        # Create Dates Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS dates (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       game_date INTEGER,
                       season INTEGER,
                       FOREIGN KEY (season) REFERENCES seasons (id)
        )''')
        
        # Create Boxscore Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS boxscores (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       home_team INTEGER,
                       away_team INTEGER,
                       game_date INTEGER,
                       url TEXT,
                       FOREIGN KEY (home_team) REFERENCES teams (id)
                       FOREIGN KEY (away_team) REFERENCES teams (id)
                       FOREIGN KEY (game_date) REFERENCES dates (id)
        )''')

        # Create Team Stats Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS team_stats (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       team INTEGER,
                       boxscore INTEGER,
                       field_goals INTEGER,
                       field_goal_attempts INTEGER,
                       three_pointers INTEGER,
                       three_point_attempts INTEGER,
                       free_throws INTEGER,
                       free_throw_attempts INTEGER,
                       offensive_rebounds INTEGER,
                       defensive_rebounds INTEGER,
                       total_rebounds INTEGER,
                       assists INTEGER,
                       steals INTEGER,
                       blocks INTEGERS,
                       turnovers INTEGER,
                       fouls INTEGER,
                       points INTEGER,
                       FOREIGN KEY (team) REFERENCES teams (id),
                       FOREIGN KEY (boxscore) REFERENCES boxscores (id)
        )''')

        # Create Players table

        cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       first_name TEXT,
                       last_name TEXT,
                       middle_name TEXT,
                       birthday TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS player_stats(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       player INTEGER,
                       team INTEGER,
                       boxscore INTEGER,
                       minutes_played INTEGER,
                       field_goals INTEGER,
                       field_goal_attempts INTEGER,
                       three_pointers INTEGER,
                       three_point_attempts INTEGER,
                       free_throws INTEGER,
                       free_throw_attempts INTEGER,
                       offensive_rebounds INTEGER,
                       defensive_rebounds INTEGER,
                       total_rebounds INTEGER,
                       assists INTEGER,
                       steals INTEGER,
                       blocks INTEGERS,
                       turnovers INTEGER,
                       fouls INTEGER,
                       points INTEGER,
                       FOREIGN KEY (player) REFERENCES players (id),
                       FOREIGN KEY (team) REFERENCES teams (id),
                       FOREIGN KEY (boxscore) REFERENCES boxscores (id)
        )''')
                
    conn.commit()

def add_season_to_table(season):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM seasons where year = ?", (season,))
        result = cursor.fetchone()

        if not result:
            cursor.execute("INSERT INTO seasons (year) VALUES (?)", (season,))
    
    conn.commit()

def add_date_to_table(date, current_season):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dates WHERE game_date = ?", (date,))
        result = cursor.fetchone()

        if not result:
            cursor.execute("SELECT * FROM seasons WHERE year = ?", (current_season,))
            season = cursor.fetchone()[0]
            
            cursor.execute("INSERT INTO dates (game_date, season) VALUES (?,?)", (date, season,))

    conn.commit()

def add_boxscore_to_table(date, home_team, away_team, url):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        # Extract PKs from database
        cursor.execute("SELECT * FROM teams where team_name = ?", (home_team,))
        home = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM teams where team_name = ?", (away_team,))
        away = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM dates where game_date = ?", (date,))
        current_date = cursor.fetchone()[0]

        # Create new boxscore entry
        cursor.execute("SELECT 1 FROM boxscores WHERE home_team = ? AND away_team = ? AND game_date = ?", (home, away, current_date))
        result = cursor.fetchone()

        if not result:
            url = 'basketball-reference.com' + url
            cursor.execute('INSERT INTO boxscores (home_team, away_team, game_date, url) VALUES (?, ?, ?, ?)', (home, away, current_date, url))

    conn.commit()
        
def add_player_stat_information(player, team, boxscore, minutes_played, field_goals, field_goal_attempts, threes, three_point_attempts,
                                free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds,
                                total_rebounds, assists, steals, blocks, turnovers, personal_fouls, points):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM player_stats WHERE player = ? AND team = ? AND boxscore = ?", (player, team, boxscore))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO player_stats (player, team, boxscore, minutes_played, field_goals, field_goal_attempts, three_pointers, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, fouls, points) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           (player, team, boxscore, minutes_played, field_goals, field_goal_attempts, threes, three_point_attempts,
                            free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists,
                            steals, blocks, turnovers, personal_fouls, points))
            
    conn.commit()

def add_team_stat_information(team, boxscore, field_goals, field_goal_attempts, threes, three_point_attempts,
                            free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, 
                            total_rebounds, assists, steals, blocks, turnovers, personal_fouls, points):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM team_stats WHERE team = ? AND boxscore = ?", (team, boxscore))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO team_stats (team, boxscore, field_goals, field_goal_attempts, three_pointers, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, fouls, points) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           (team, boxscore, field_goals, field_goal_attempts, threes, three_point_attempts,
                            free_throws, free_throw_attempts, offensive_rebounds, defensive_rebounds, total_rebounds, assists,
                            steals, blocks, turnovers, personal_fouls, points))
            
    conn.commit()

def add_model_to_table(model, name="UNNAMED", algorithm_type=None):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM trained_models WHERE model_name = ? AND algorithm_id = ?", (name, algorithm_type))

        result = cursor.fetchone()

        if result:
            return "Model name is already present in database -  rename model and try again."
        else:
            cursor.execute('INSERT INTO trained_models (algorithm_id, model_name, active_model) VALUES (?, ?, ?)',
                           (algorithm_type, name, model))
            
    conn.commit()

def add_bet_to_table(model_id, money_staked, line, bet_type_id, winner, gain_loss, boxscore_id):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = f"""
        INSERT INTO bets_placed (model_id, money_staked, line, bet_type_id, winner, gain_loss, boxscore_id)
        VALUES
        ({model_id}, {money_staked}, {line}, {bet_type_id}, {winner}, {gain_loss}, {boxscore_id})
        """

        cursor.execute(sql_statement)

    conn.commit()

########### QUERIES FOR EXTRACTING INFORMATION FROM DATABASE ######################
def search_games_by_date(date):

    #Convert date to proper form - if for some reason the date is unreadable, send an error to the user.
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """
        SELECT 
        dates.game_date as date,
        ht.team_name AS home_team_name,
        at.team_name AS away_team_name
        FROM boxscores
        LEFT JOIN dates on boxscores.game_date = dates.id
        LEFT JOIN teams as ht on boxscores.home_team = ht.id
        LEFT JOIN teams as at on boxscores.away_team = at.id 
        WHERE dates.game_date = ?
        """
        cursor.execute(sql_statement, (str(date),))
        results = []
        columns = [desc[0] for desc in cursor.description] 
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

    return results
    #Try to see if the date exists in the db
    #If not, return a json string saying "No games were played on that date"

def retrieve_date_id(game_date):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dates WHERE game_date = '{}'".format(game_date))
        date_id = cursor.fetchone()[0]

        return date_id

def retrieve_team_abbrv(team_id):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM boxscores WHERE home_team = '{}'".format(team_id))
        abbrv = cursor.fetchone()[0][-8:-5]

        return abbrv

def retrieve_all_boxscores():
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM boxscores")
        boxscores = cursor.fetchall()

        return boxscores

def retrieve_yesterdays_boxscores(date_id):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, url FROM boxscores WHERE game_date = {}".format(date_id))
        
        boxscores = cursor.fetchall()

        return boxscores

def retrieve_boxscores(year, month = None, day = None):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        if day != None and month != None:
            sql_statement = """
            SELECT 
            boxscores.id,
            boxscores.url
            FROM boxscores
            JOIN dates ON boxscores.game_date = dates.id
            WHERE SUBSTR(dates.game_date, 1, 4) = '{}'
            AND SUBSTR(dates.game_date, 6, 2) = '{}'
            AND SUBSTR(dates.game_date, 9, 2) = '{}';
            """.format(year, month, day)

        if day == None and month != None:
            sql_statement = """
            SELECT 
            boxscores.id,
            boxscores.url
            FROM boxscores
            JOIN dates ON boxscores.game_date = dates.id
            WHERE SUBSTR(dates.game_date, 1, 4) = '{}'
            AND SUBSTR(dates.game_date, 6, 2) = '{}';
            """.format(year, month)

        if day == None and month == None:

            sql_statement = """
            SELECT 
            boxscores.id,
            boxscores.url
            FROM boxscores
            JOIN dates ON boxscores.game_date = dates.id
            WHERE SUBSTR(dates.game_date, 1, 4) = '{}';
            """.format(year)

        cursor.execute(sql_statement)
        boxscores = cursor.fetchall()

        return boxscores

def retrieve_player_information(first_name, middle_name, last_name, birthday):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM players WHERE first_name = ? and middle_name = ? and last_name = ? and birthday = ?", (first_name, middle_name, last_name, birthday))
        result = cursor.fetchone()

        if not result:
            cursor.execute("INSERT INTO players (first_name, middle_name, last_name, birthday) VALUES (?, ?, ?, ?)", (first_name, middle_name, last_name, birthday))
            conn.commit()
            time.sleep(1)
            cursor.execute("SELECT * FROM players WHERE first_name = ? and middle_name = ? and last_name = ? and birthday = ?", (first_name, middle_name, last_name, birthday))
            result = cursor.fetchone()
        
        return result

def retrieve_team_information(team_name):
    
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM teams WHERE team_name = ?", (team_name,))
        result = cursor.fetchone()

    return result

def get_player_stats_for_season(first_name, last_name, season):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """
        SELECT 
            players.first_name as First,
            players.middle_name as Middle,
            players.last_name as Last,
            teams.team_name as Team,
            COALESCE(opponent_teams.team_name, 'Unknown') as Opponent,
            dates.game_date as date,
            player_stats.minutes_played as Minutes,
            player_stats.points as PTs,
            player_stats.field_goals as FGs,
            player_stats.field_goal_attempts as FGA,
            player_stats.three_pointers as Ts,
            player_stats.three_point_attempts as TPA,
            player_stats.free_throws as FTs,
            player_stats.free_throw_attempts as FTA,
            player_stats.offensive_rebounds as ORB,
            player_stats.defensive_rebounds as DRB,
            player_stats.total_rebounds as TRB,
            player_stats.assists as ASTs,
            player_stats.steals as STLs,
            player_stats.blocks as BLKs,
            player_stats.turnovers as TOs,
            player_stats.fouls as Fouls
            FROM player_stats
            LEFT JOIN players ON player_stats.player = players.id
            LEFT JOIN boxscores on player_stats.boxscore = boxscores.id
            LEFT JOIN dates on boxscores.game_date = dates.id
            LEFT JOIN teams on player_stats.team = teams.id
            LEFT JOIN teams AS opponent_teams ON 
                CASE 
                    WHEN player_stats.team = boxscores.home_team THEN boxscores.away_team
                    ELSE boxscores.home_team
                END = opponent_teams.id
            LEFT JOIN seasons ON dates.season = seasons.id
            WHERE players.first_name = ? and players.last_name = ? and seasons.year = ?
        """

        cursor.execute(sql_statement, (first_name, last_name, season))
        results = []
        columns = [desc[0] for desc in cursor.description] 
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

    return results
#Get player stats on a specific date
def get_player_stats_for_date(first_name, last_name, date):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """
        SELECT 
            players.first_name as First,
            players.middle_name as Middle,
            players.last_name as Last,
            teams.team_name as Team,
            COALESCE(opponent_teams.team_name, 'Unknown') as Opponent,
            dates.game_date as date,
            player_stats.minutes_played as Minutes,
            player_stats.points as PTs,
            player_stats.field_goals as FGs,
            player_stats.field_goal_attempts as FGA,
            player_stats.three_pointers as Ts,
            player_stats.three_point_attempts as TPA,
            player_stats.free_throws as FTs,
            player_stats.free_throw_attempts as FTA,
            player_stats.offensive_rebounds as ORB,
            player_stats.defensive_rebounds as DRB,
            player_stats.total_rebounds as TRB,
            player_stats.assists as ASTs,
            player_stats.steals as STLs,
            player_stats.blocks as BLKs,
            player_stats.turnovers as TOs,
            player_stats.fouls as Fouls
            FROM player_stats
            LEFT JOIN players ON player_stats.player = players.id
            LEFT JOIN boxscores on player_stats.boxscore = boxscores.id
            LEFT JOIN dates on boxscores.game_date = dates.id
            LEFT JOIN teams on player_stats.team = teams.id
            LEFT JOIN teams AS opponent_teams ON 
                CASE 
                    WHEN player_stats.team = boxscores.home_team THEN boxscores.away_team
                    ELSE boxscores.home_team
                END = opponent_teams.id
            WHERE players.first_name = ? and players.last_name = ? and dates.game_date = ?
        """

        cursor.execute(sql_statement, (first_name, last_name, date))
        results = []
        columns = [desc[0] for desc in cursor.description] 
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

    return results
#Get team stats for a specific date
def get_team_stats_for_date(team_name, date):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """ 
        SELECT 
            teams.team_name as Team,
            COALESCE(opponent_teams.team_name, 'Unknown') as Opponent,
            dates.game_date as date,
            team_stats.points as PTs,
            team_stats.field_goals as FGs,
            team_stats.field_goal_attempts as FGA,
            team_stats.three_pointers as Ts,
            team_stats.three_point_attempts as TPA,
            team_stats.free_throws as FTs,
            team_stats.free_throw_attempts as FTA,
            team_stats.offensive_rebounds as ORB,
            team_stats.defensive_rebounds as DRB,
            team_stats.total_rebounds as TRB,
            team_stats.assists as ASTs,
            team_stats.steals as STLs,
            team_stats.blocks as BLKs,
            team_stats.turnovers as TOs,
            team_stats.fouls as Fouls
            FROM team_stats
            LEFT JOIN boxscores on team_stats.boxscore = boxscores.id
            LEFT JOIN dates on boxscores.game_date = dates.id
            LEFT JOIN teams on team_stats.team = teams.id
            LEFT JOIN teams AS opponent_teams ON 
                CASE 
                    WHEN team_stats.team = boxscores.home_team THEN boxscores.away_team
                    ELSE boxscores.home_team
                END = opponent_teams.id
            LEFT JOIN seasons ON dates.season = seasons.id
            WHERE teams.team_name = ? and dates.game_date = ?
        """
        cursor.execute(sql_statement, (team_name, date))
        results = cursor.fetchall()

    return results

#Get all team stats for a season
def get_team_stats_for_season(team_name, season):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """
        SELECT 
            teams.team_name as Team,
            COALESCE(opponent_teams.team_name, 'Unknown') as Opponent,
            dates.game_date as date,
            team_stats.points as PTs,
            team_stats.field_goals as FGs,
            team_stats.field_goal_attempts as FGA,
            team_stats.three_pointers as Ts,
            team_stats.three_point_attempts as TPA,
            team_stats.free_throws as FTs,
            team_stats.free_throw_attempts as FTA,
            team_stats.offensive_rebounds as ORB,
            team_stats.defensive_rebounds as DRB,
            team_stats.total_rebounds as TRB,
            team_stats.assists as ASTs,
            team_stats.steals as STLs,
            team_stats.blocks as BLKs,
            team_stats.turnovers as TOs,
            team_stats.fouls as Fouls
            FROM team_stats
            LEFT JOIN boxscores on team_stats.boxscore = boxscores.id
            LEFT JOIN dates on boxscores.game_date = dates.id
            LEFT JOIN teams on team_stats.team = teams.id
            LEFT JOIN teams AS opponent_teams ON 
                CASE 
                    WHEN team_stats.team = boxscores.home_team THEN boxscores.away_team
                    ELSE boxscores.home_team
                END = opponent_teams.id
            LEFT JOIN seasons ON dates.season = seasons.id
        WHERE teams.team_name = ? and seasons.year = ?
        """

        cursor.execute(sql_statement, (team_name, season))
        results = []
        columns = [desc[0] for desc in cursor.description]
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

    return results

def get_all_team_names():
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """
        SELECT team_name from teams
        """

        cursor.execute(sql_statement)
        results = cursor.fetchall()

    return results

def get_team_name_by_id(id):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = f"""
        SELECT team_name from teams where id = {id}
        """

        cursor.execute(sql_statement)
        results = cursor.fetchone()[0]

    return results

def get_gamma_training_data():

    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = """
    WITH TeamStats as (
    SELECT
        boxscore,
        team,
        AVG(field_goals) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS field_goals,
        AVG(field_goal_attempts) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS field_goal_attempts,
        AVG(three_pointers) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS three_pointers,
        AVG(three_point_attempts) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS three_point_attempts,
        AVG(free_throws) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS free_throws,
        AVG(free_throw_attempts) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS free_throw_attempts,
        AVG(offensive_rebounds) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS offensive_rebounds,
        AVG(defensive_rebounds) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS defensive_rebounds,
        AVG(total_rebounds) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS total_rebounds,
        AVG(assists) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS assists,
        AVG(steals) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS steals,
        AVG(blocks) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS blocks,
        AVG(turnovers) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS turnovers,
        AVG(fouls) OVER (PARTITION BY team ORDER BY boxscore ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS fouls,
        points
    FROM 
        team_stats
    LIMIT -1 OFFSET 2
    )

    SELECT 
        dates.season,
        t1.boxscore,
        boxscores.home_team AS home_team,
        boxscores.away_team AS away_team,
        CASE
            WHEN t1.team = home_team THEN
            (2*t1.field_goals) - (2*(t1.field_goal_attempts - t1.field_goals)) + (3*t1.three_pointers) - (3*(t1.three_point_attempts-t1.three_pointers)) +
            t1.free_throws - (t1.free_throw_attempts-t1.free_throws) + t1.offensive_rebounds + t1.defensive_rebounds +
            (0.5*t1.assists) + t1.steals + t1.blocks - t1.turnovers
            WHEN t2.team = home_team THEN
            (2*t2.field_goals) - (2*(t2.field_goal_attempts - t2.field_goals)) + (3*t2.three_pointers) - (3*(t2.three_point_attempts-t2.three_pointers)) +
            t2.free_throws - (t2.free_throw_attempts-t2.free_throws) + t2.offensive_rebounds + t2.defensive_rebounds +
            (0.5*t2.assists) + t2.steals + t2.blocks - t2.turnovers
            ELSE NULL
        END AS home_gamma,
        
        CASE
            WHEN t1.team = away_team THEN
            (2*t1.field_goals) - (2*(t1.field_goal_attempts - t1.field_goals)) + (3*t1.three_pointers) - (3*(t1.three_point_attempts-t1.three_pointers)) +
            t1.free_throws - (t1.free_throw_attempts-t1.free_throws) + t1.offensive_rebounds + t1.defensive_rebounds +
            (0.5*t1.assists) + t1.steals + t1.blocks - t1.turnovers
            WHEN t2.team = away_team THEN
            (2*t2.field_goals) - (2*(t2.field_goal_attempts - t2.field_goals)) + (3*t2.three_pointers) - (3*(t2.three_point_attempts-t2.three_pointers)) +
            t2.free_throws - (t2.free_throw_attempts-t2.free_throws) + t2.offensive_rebounds + t2.defensive_rebounds +
            (0.5*t2.assists) + t2.steals + t2.blocks - t2.turnovers
            ELSE NULL
        END AS away_gamma,

        CASE
            WHEN t1.team = home_team THEN t1.points
            WHEN t2.team = home_team THEN t2.points
        END AS home_points,
        
        CASE
            WHEN t1.team = away_team THEN t1.points
            WHEN t2.team = away_team THEN t2.points
        END AS away_points,
        
        CASE 
            WHEN t1.team = home_team THEN t1.points - t2.points + odds.homeline
            WHEN t2.team = home_team THEN t2.points - t1.points + odds.homeline
        END as covered,
        
        odds.homeline as homeline


    FROM
        TeamStats t1
    JOIN TeamStats t2 ON t1.boxscore = t2.boxscore AND t1.team < t2.team
    JOIN boxscores on t1.boxscore = boxscores.id
    JOIN odds on odds.boxscore = boxscores.id
    JOIN dates on boxscores.game_date = dates.id
    WHERE dates.season in (4,5)
    """

    cursor.execute(sql_statement)
    results = cursor.fetchall()

    return results

def get_team_boxscore_stats_nday_moving_average(n_days, season):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = f"""
        WITH TeamAverages AS(
            SELECT
            boxscore,
            team,
            dates.game_date,
            dates.season,
            AVG(field_goals) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as field_goals,
            AVG(field_goal_attempts) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as field_goal_attempts,
            AVG(three_pointers) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as three_pointers,
            AVG(three_point_attempts) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as three_point_attempts,
            AVG(free_throws) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as free_throws,
            AVG(free_throw_attempts) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as free_throw_attempts,
            AVG(offensive_rebounds) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as offensive_rebounds,
            AVG(defensive_rebounds) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as defensive_rebounds,
            AVG(total_rebounds) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as total_rebounds,
            AVG(assists) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as assists,
            AVG(steals) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as steals,
            AVG(blocks) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as blocks,
            AVG(turnovers) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as turnovers,
            AVG(fouls) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as fouls,
            AVG(points) OVER (PARTITION BY team_stats.team, dates.season ORDER BY dates.game_date ROWS BETWEEN {n_days} PRECEDING AND 1 PRECEDING) as avg_points,
            points
            FROM team_stats
            JOIN boxscores on team_stats.boxscore = boxscores.id
            JOIN dates on boxscores.game_date = dates.id
            WHERE dates.season = {season}
            LIMIT -1 OFFSET {n_days}
            )

            SELECT
            t1.boxscore,
            dates.game_date,
            dates.season,
            boxscores.home_team as home_team,
            boxscores.away_team as away_team,
            
            CASE
                WHEN t1.team = home_team THEN t1.avg_points
                WHEN t2.team = home_team THEN t2.avg_points
                ELSE NULL
            END AS home_avg_points,

            CASE
                WHEN t1.team = home_team THEN t1.field_goals
                WHEN t2.team = home_team THEN t2.field_goals
                ELSE NULL
            END AS home_field_goals,
            
            CASE
                WHEN t1.team = home_team THEN t1.field_goal_attempts
                WHEN t2.team = home_team THEN t2.field_goal_attempts
                ELSE NULL
            END AS home_field_goal_attempts,
            
            CASE
                WHEN t1.team = home_team THEN t1.three_pointers
                WHEN t2.team = home_team THEN t2.three_pointers
                ELSE NULL
            END AS home_three_pointers,
            
            CASE
                WHEN t1.team = home_team THEN t1.three_point_attempts
                WHEN t2.team = home_team THEN t2.three_point_attempts
                ELSE NULL
            END AS home_three_point_attempts,
            
            CASE
                WHEN t1.team = home_team THEN t1.free_throws
                WHEN t2.team = home_team THEN t2.free_throws
                ELSE NULL
            END AS home_free_throws,
            
            CASE
                WHEN t1.team = home_team THEN t1.free_throw_attempts
                WHEN t2.team = home_team THEN t2.free_throw_attempts
                ELSE NULL
            END AS home_free_throw_attempts,
            
            CASE
                WHEN t1.team = home_team THEN t1.offensive_rebounds
                WHEN t2.team = home_team THEN t2.offensive_rebounds
                ELSE NULL
            END AS home_offensive_rebounds,
            
            CASE
                WHEN t1.team = home_team THEN t1.defensive_rebounds
                WHEN t2.team = home_team THEN t2.defensive_rebounds
                ELSE NULL
            END AS home_defensive_rebounds,
            
            CASE
                WHEN t1.team = home_team THEN t1.total_rebounds
                WHEN t2.team = home_team THEN t2.total_rebounds
                ELSE NULL
            END AS home_total_rebounds,
            
            CASE
                WHEN t1.team = home_team THEN t1.assists
                WHEN t2.team = home_team THEN t2.assists
                ELSE NULL
            END AS home_assists,
            
            CASE
                WHEN t1.team = home_team THEN t1.steals
                WHEN t2.team = home_team THEN t2.steals
                ELSE NULL
            END AS home_steals,
            
            CASE
                WHEN t1.team = home_team THEN t1.blocks
                WHEN t2.team = home_team THEN t2.blocks
                ELSE NULL
            END AS home_blocks,
            
            CASE
                WHEN t1.team = home_team THEN t1.turnovers
                WHEN t2.team = home_team THEN t2.turnovers
                ELSE NULL
            END AS home_turnovers,
            
            CASE
                WHEN t1.team = home_team THEN t1.fouls
                WHEN t2.team = home_team THEN t2.fouls
                ELSE NULL
            END AS home_fouls,
            
            CASE
                WHEN t1.team = away_team THEN t1.avg_points
                WHEN t2.team = away_team THEN t2.avg_points
                ELSE NULL
            END AS away_avg_points,

            CASE
                WHEN t1.team = away_team THEN t1.field_goals
                WHEN t2.team = away_team THEN t2.field_goals
                ELSE NULL
            END AS away_field_goals,
            
            CASE
                WHEN t1.team = away_team THEN t1.field_goal_attempts
                WHEN t2.team = away_team THEN t2.field_goal_attempts
                ELSE NULL
            END AS away_field_goal_attempts,
            
            CASE
                WHEN t1.team = away_team THEN t1.three_pointers
                WHEN t2.team = away_team THEN t2.three_pointers
                ELSE NULL
            END AS away_three_pointers,
            
            CASE
                WHEN t1.team = away_team THEN t1.three_point_attempts
                WHEN t2.team = away_team THEN t2.three_point_attempts
                ELSE NULL
            END AS away_three_point_attempts,
            
            CASE
                WHEN t1.team = away_team THEN t1.free_throws
                WHEN t2.team = away_team THEN t2.free_throws
                ELSE NULL
            END AS away_free_throws,
            
            CASE
                WHEN t1.team = away_team THEN t1.free_throw_attempts
                WHEN t2.team = away_team THEN t2.free_throw_attempts
                ELSE NULL
            END AS away_free_throw_attempts,
            
            CASE
                WHEN t1.team = away_team THEN t1.offensive_rebounds
                WHEN t2.team = away_team THEN t2.offensive_rebounds
                ELSE NULL
            END AS away_offensive_rebounds,
            
            CASE
                WHEN t1.team = away_team THEN t1.defensive_rebounds
                WHEN t2.team = away_team THEN t2.defensive_rebounds
                ELSE NULL
            END AS away_defensive_rebounds,
            
            CASE
                WHEN t1.team = away_team THEN t1.total_rebounds
                WHEN t2.team = away_team THEN t2.total_rebounds
                ELSE NULL
            END AS away_total_rebounds,
            
            CASE
                WHEN t1.team = away_team THEN t1.assists
                WHEN t2.team = away_team THEN t2.assists
                ELSE NULL
            END AS away_assists,
            
            CASE
                WHEN t1.team = away_team THEN t1.steals
                WHEN t2.team = away_team THEN t2.steals
                ELSE NULL
            END AS away_steals,
            
            CASE
                WHEN t1.team = away_team THEN t1.blocks
                WHEN t2.team = away_team THEN t2.blocks
                ELSE NULL
            END AS away_blocks,
            
            CASE
                WHEN t1.team = away_team THEN t1.turnovers
                WHEN t2.team = away_team THEN t2.turnovers
                ELSE NULL
            END AS away_turnovers,
            
            CASE
                WHEN t1.team = away_team THEN t1.fouls
                WHEN t2.team = away_team THEN t2.fouls
                ELSE NULL
            END AS away_fouls,
            
            CASE
                WHEN t1.team = home_team THEN t1.points
                WHEN t2.team = home_team THEN t2.points
            END AS home_points,
                
            CASE
                WHEN t1.team = away_team THEN t1.points
                WHEN t2.team = away_team THEN t2.points
            END AS away_points,
            
            odds.homeline as homeline
            
            FROM 
                TeamAverages t1
            JOIN TeamAverages t2 on t1.boxscore = t2.boxscore AND t1.team < t2.team
            JOIN boxscores on t1.boxscore = boxscores.id
            JOIN odds on odds.boxscore = boxscores.id
            JOIN dates on boxscores.game_date = dates.id
            WHERE dates.season = {season}
        """

    cursor.execute(sql_statement)
    results = cursor.fetchall()

    columns = ['boxscore','game_date', 'season', 'home_team', 'away_team', 'home_avg_points', 'home_field_goals', 'home_field_goal_attempts', 'home_threes', 'home_three_point_attempts',
               'home_free_throws', 'home_free_throw_attempts', 'home_offensive_rebounds', 'home_defensive_rebounds', 'home_total_rebounds', 'home_assists', 'home_steals',
               'home_blocks', 'home_turnovers', 'home_fouls', 'away_avg_points', 'away_field_goals', 'away_field_goal_attempts', 'away_threes', 'away_three_point_attempts',
               'away_free_throws', 'away_free_throw_attempts', 'away_offensive_rebounds', 'away_defensive_rebounds', 'away_total_rebounds', 'away_assists', 'away_steals',
               'away_blocks', 'away_turnovers', 'away_fouls', 'home_points', 'away_points', 'home_spread']

    df = pd.DataFrame(results, columns=columns).dropna()

    def spread_covered(row):
        home_points_spread = row['home_points'] + row['home_spread']
        if home_points_spread > row['away_points']:
            return 1
        else:
            return 0

    df['covered'] = df.apply(spread_covered, axis=1)

    return df

def get_team_boxscore_stats_include_opponent_stats(n_days, season):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = f"""
        SELECT 
        team_stats.boxscore,
        dates.game_date,
        SUBSTR(GROUP_CONCAT(team_stats.team), INSTR(GROUP_CONCAT(team_stats.team), ',') + 1) AS home_team,
        SUBSTR(GROUP_CONCAT(team_stats.team), 1 ,INSTR(GROUP_CONCAT(team_stats.team), ',') - 1) AS away_team,

        SUBSTR(GROUP_CONCAT(team_stats.points), INSTR(GROUP_CONCAT(team_stats.points), ',') + 1) AS home_points,
        SUBSTR(GROUP_CONCAT(team_stats.field_goals), INSTR(GROUP_CONCAT(team_stats.field_goals), ',') + 1) AS home_field_goals,
        SUBSTR(GROUP_CONCAT(team_stats.field_goal_attempts), INSTR(GROUP_CONCAT(team_stats.field_goal_attempts), ',') + 1) AS home_field_goal_attempts,
        SUBSTR(GROUP_CONCAT(team_stats.three_pointers), INSTR(GROUP_CONCAT(team_stats.three_pointers), ',') + 1) AS home_three_pointers,
        SUBSTR(GROUP_CONCAT(team_stats.three_point_attempts), INSTR(GROUP_CONCAT(team_stats.three_point_attempts), ',') + 1) AS home_three_point_attempts,
        SUBSTR(GROUP_CONCAT(team_stats.free_throws), INSTR(GROUP_CONCAT(team_stats.free_throws), ',') + 1) AS home_free_throws,
        SUBSTR(GROUP_CONCAT(team_stats.free_throw_attempts), INSTR(GROUP_CONCAT(team_stats.free_throw_attempts), ',') + 1) AS home_free_throw_attempts,
        SUBSTR(GROUP_CONCAT(team_stats.offensive_rebounds), INSTR(GROUP_CONCAT(team_stats.offensive_rebounds), ',') + 1) AS home_offensive_rebounds,
        SUBSTR(GROUP_CONCAT(team_stats.defensive_rebounds), INSTR(GROUP_CONCAT(team_stats.defensive_rebounds), ',') + 1) AS home_defensive_rebounds,
        SUBSTR(GROUP_CONCAT(team_stats.total_rebounds), INSTR(GROUP_CONCAT(team_stats.total_rebounds), ',') + 1) AS home_total_rebounds,
        SUBSTR(GROUP_CONCAT(team_stats.assists), INSTR(GROUP_CONCAT(team_stats.assists), ',') + 1) AS home_assists,
        SUBSTR(GROUP_CONCAT(team_stats.steals), INSTR(GROUP_CONCAT(team_stats.steals), ',') + 1) AS home_steals,
        SUBSTR(GROUP_CONCAT(team_stats.blocks), INSTR(GROUP_CONCAT(team_stats.blocks), ',') + 1) AS home_blocks,
        SUBSTR(GROUP_CONCAT(team_stats.turnovers), INSTR(GROUP_CONCAT(team_stats.turnovers), ',') + 1) AS home_turnovers,
        SUBSTR(GROUP_CONCAT(team_stats.fouls), INSTR(GROUP_CONCAT(team_stats.fouls), ',') + 1) AS home_fouls,

        SUBSTR(GROUP_CONCAT(team_stats.points), 1 ,INSTR(GROUP_CONCAT(team_stats.points), ',') - 1) AS away_points,
        SUBSTR(GROUP_CONCAT(team_stats.field_goals), 1 ,INSTR(GROUP_CONCAT(team_stats.field_goals), ',') - 1) AS away_field_goals,
        SUBSTR(GROUP_CONCAT(team_stats.field_goal_attempts), 1 ,INSTR(GROUP_CONCAT(team_stats.field_goal_attempts), ',') - 1) AS away_field_goal_attempts,
        SUBSTR(GROUP_CONCAT(team_stats.three_pointers), 1 ,INSTR(GROUP_CONCAT(team_stats.three_pointers), ',') - 1) AS away_three_pointers,
        SUBSTR(GROUP_CONCAT(team_stats.three_point_attempts), 1 ,INSTR(GROUP_CONCAT(team_stats.three_point_attempts), ',') - 1) AS away_three_point_attempts,
        SUBSTR(GROUP_CONCAT(team_stats.free_throws), 1 ,INSTR(GROUP_CONCAT(team_stats.free_throws), ',') - 1) AS away_free_throws,
        SUBSTR(GROUP_CONCAT(team_stats.free_throw_attempts), 1 ,INSTR(GROUP_CONCAT(team_stats.free_throw_attempts), ',') - 1) AS away_free_throw_attempts,
        SUBSTR(GROUP_CONCAT(team_stats.offensive_rebounds), 1 ,INSTR(GROUP_CONCAT(team_stats.offensive_rebounds), ',') - 1) AS away_offensive_rebounds,
        SUBSTR(GROUP_CONCAT(team_stats.defensive_rebounds), 1 ,INSTR(GROUP_CONCAT(team_stats.defensive_rebounds), ',') - 1) AS away_defensive_rebounds,
        SUBSTR(GROUP_CONCAT(team_stats.total_rebounds), 1 ,INSTR(GROUP_CONCAT(team_stats.total_rebounds), ',') - 1) AS away_total_rebounds,
        SUBSTR(GROUP_CONCAT(team_stats.assists), 1 ,INSTR(GROUP_CONCAT(team_stats.assists), ',') - 1) AS away_assists,
        SUBSTR(GROUP_CONCAT(team_stats.steals), 1 ,INSTR(GROUP_CONCAT(team_stats.steals), ',') - 1) AS away_steals,
        SUBSTR(GROUP_CONCAT(team_stats.blocks), 1 ,INSTR(GROUP_CONCAT(team_stats.blocks), ',') - 1) AS away_blocks,
        SUBSTR(GROUP_CONCAT(team_stats.turnovers), 1 ,INSTR(GROUP_CONCAT(team_stats.turnovers), ',') - 1) AS away_turnovers,
        SUBSTR(GROUP_CONCAT(team_stats.fouls), 1 ,INSTR(GROUP_CONCAT(team_stats.fouls), ',') - 1) AS away_fouls,
        odds.homeline as home_spread,
        odds.OU as over_under

        FROM team_stats
        JOIN boxscores on team_stats.boxscore = boxscores.id
        JOIN dates on dates.id = boxscores.game_date
        JOIN odds on odds.boxscore = boxscores.id
        WHERE dates.season = {season}
        GROUP BY team_stats.boxscore
        ORDER BY 
            CASE
                WHEN home_team = 1 THEN 1
                WHEN away_team = 1 THEN 1
                WHEN home_team = 2 THEN 2
                WHEN away_team = 2 THEN 2
                WHEN home_team = 3 THEN 3
                WHEN away_team = 3 THEN 3
                WHEN home_team = 4 THEN 4
                WHEN away_team = 4 THEN 4
                WHEN home_team = 5 THEN 5
                WHEN away_team = 5 THEN 5
                WHEN home_team = 6 THEN 6
                WHEN away_team = 6 THEN 6
                WHEN home_team = 7 THEN 7
                WHEN away_team = 7 THEN 7
                WHEN home_team = 8 THEN 8
                WHEN away_team = 8 THEN 8
                WHEN home_team = 9 THEN 9
                WHEN away_team = 9 THEN 9
                WHEN home_team = 10 THEN 10
                WHEN away_team = 10 THEN 10
                WHEN home_team = 11 THEN 11
                WHEN away_team = 11 THEN 11
                WHEN home_team = 12 THEN 12
                WHEN away_team = 12 THEN 12
                WHEN home_team = 13 THEN 13
                WHEN away_team = 13 THEN 13
                WHEN home_team = 14 THEN 14
                WHEN away_team = 14 THEN 14
                WHEN home_team = 15 THEN 15
                WHEN away_team = 15 THEN 15
                WHEN home_team = 16 THEN 16
                WHEN away_team = 16 THEN 16
                WHEN home_team = 17 THEN 17
                WHEN away_team = 17 THEN 17
                WHEN home_team = 18 THEN 18
                WHEN away_team = 18 THEN 18
                WHEN home_team = 19 THEN 19
                WHEN away_team = 19 THEN 19
                WHEN home_team = 20 THEN 20
                WHEN away_team = 20 THEN 20
                WHEN home_team = 21 THEN 21
                WHEN away_team = 21 THEN 21
                WHEN home_team = 22 THEN 22
                WHEN away_team = 22 THEN 22
                WHEN home_team = 23 THEN 23
                WHEN away_team = 23 THEN 23
                WHEN home_team = 24 THEN 24
                WHEN away_team = 24 THEN 24
                WHEN home_team = 25 THEN 25
                WHEN away_team = 25 THEN 25
                WHEN home_team = 26 THEN 26
                WHEN away_team = 26 THEN 26
                WHEN home_team = 27 THEN 27
                WHEN away_team = 27 THEN 27
                WHEN home_team = 28 THEN 28
                WHEN away_team = 28 THEN 28
                WHEN home_team = 29 THEN 29
                WHEN away_team = 29 THEN 29
                WHEN home_team = 30 THEN 30
                WHEN away_team = 30 THEN 30
            END,
            dates.game_date
        """

        cursor.execute(sql_statement)
        results = cursor.fetchall()

        columns = ['boxscore', 'game_date', 'home_team', 'away_team', 'home_points', 'home_field_goals', 'home_field_goal_attempts',
                   'home_three_pointers', 'home_three_point_attempts', 'home_free_throws', 'home_free_throw_attempts', 'home_offensive_rebounds',
                   'home_defensive_rebounds', 'home_total_rebounds', 'home_assists', 'home_steals', 'home_blocks', 'home_turnovers', 'home_fouls',
                   'away_points', 'away_field_goals', 'away_field_goal_attempts', 'away_three_pointers', 'away_three_point_attempts', 
                   'away_free_throws', 'away_free_throw_attempts', 'away_offensive_rebounds', 'away_defensive_rebounds', 'away_total_rebounds', 
                   'away_assists', 'away_steals', 'away_blocks', 'away_turnovers', 'away_fouls', 'spread', 'over_under']
        
        df = pd.DataFrame(results, columns=columns).dropna()

        def spread_covered(row):
            home_points_spread = float(row['home_points']) + float(row['spread'])
            if home_points_spread > float(row['away_points']):
                return 1
            else:
                return 0
            
        def over_under_covered(row):
            total_points = float(row['home_points']) + float(row['away_points'])

            if total_points > float(row['over_under']):
                return 1
            else:
                return 0

        df['spread_covered'] = df.apply(spread_covered, axis=1)
        df['points_covered'] = df.apply(over_under_covered, axis=1)

    teams = np.arange(1,31)

    team_dataframes = []


    for team in teams:
        home_team_condition = (df['home_team'] == str(team))
        if not df['home_team'].empty:
            team_df = df[home_team_condition]
            holder_df = team_df[['boxscore', 'game_date','spread', 'over_under', 'spread_covered', 'points_covered']]
            team_stats = team_df.filter(like='home')
            team_stats = team_stats[team_stats['home_team'] == str(team)]
            opp_stats = team_df.filter(like='away')
            opp_stats = opp_stats[opp_stats['away_team'] != str(team)]

            home_df = pd.concat([holder_df, team_stats, opp_stats], axis=1, ignore_index=False)

            home_df = home_df.rename(columns={
                'home_team': 'team',
                'home_points': 'points',
                'home_field_goals': 'field_goals',
                'home_field_goal_attempts': 'field_goal_attempts',
                'home_three_pointers': 'three_pointers',
                'home_three_point_attempts': 'three_point_attempts',
                'home_free_throws': 'free_throws',
                'home_free_throw_attempts': 'free_throw_attempts',
                'home_offensive_rebounds': 'offensive_rebounds',
                'home_defensive_rebounds': 'defensive_rebounds',
                'home_total_rebounds': 'total_rebounds',
                'home_assists': 'assists',
                'home_steals': 'steals',
                'home_blocks': 'blocks',
                'home_turnovers': 'turnovers',
                'home_fouls': 'fouls',
                'away_team': 'opp_team',
                'away_points': 'opp_points',
                'away_field_goals': 'opp_field_goals',
                'away_field_goal_attempts': 'opp_field_goal_attempts',
                'away_three_pointers': 'opp_three_pointers',
                'away_three_point_attempts': 'opp_three_point_attempts',
                'away_free_throws': 'opp_free_throws',
                'away_free_throw_attempts': 'opp_free_throw_attempts',
                'away_offensive_rebounds': 'opp_offensive_rebounds',
                'away_defensive_rebounds': 'opp_defensive_rebounds',
                'away_total_rebounds': 'opp_total_rebounds',
                'away_assists': 'opp_assists',
                'away_steals': 'opp_steals',
                'away_blocks': 'opp_blocks',
                'away_turnovers': 'opp_turnovers',
                'away_fouls': 'opp_fouls'
            })

        away_team_condition = (df['away_team'] == str(team))
        if not df['away_team'].empty:
            team_df = df[away_team_condition]
            holder_df = team_df[['boxscore', 'game_date','spread', 'over_under', 'spread_covered', 'points_covered']]
            team_stats = team_df.filter(like='away')
            team_stats = team_stats[team_stats['away_team'] == str(team)]

            opp_stats = team_df.filter(like='home')
            opp_stats = opp_stats[opp_stats['home_team'] != str(team)]

            away_df = pd.concat([holder_df, opp_stats, team_stats], axis=1, ignore_index=False)

            away_df = away_df.rename(columns={
                'home_team': 'opp_team',
                'home_points': 'opp_points',
                'home_field_goals': 'opp_field_goals',
                'home_field_goal_attempts': 'opp_field_goal_attempts',
                'home_three_pointers': 'opp_three_pointers',
                'home_three_point_attempts': 'opp_three_point_attempts',
                'home_free_throws': 'opp_free_throws',
                'home_free_throw_attempts': 'opp_free_throw_attempts',
                'home_offensive_rebounds': 'opp_offensive_rebounds',
                'home_defensive_rebounds': 'opp_defensive_rebounds',
                'home_total_rebounds': 'opp_total_rebounds',
                'home_assists': 'opp_assists',
                'home_steals': 'opp_steals',
                'home_blocks': 'opp_blocks',
                'home_turnovers': 'opp_turnovers',
                'home_fouls': 'opp_fouls',
                'away_team': 'team',
                'away_points': 'points',
                'away_field_goals': 'field_goals',
                'away_field_goal_attempts': 'field_goal_attempts',
                'away_three_pointers': 'three_pointers',
                'away_three_point_attempts': 'three_point_attempts',
                'away_free_throws': 'free_throws',
                'away_free_throw_attempts': 'free_throw_attempts',
                'away_offensive_rebounds': 'offensive_rebounds',
                'away_defensive_rebounds': 'defensive_rebounds',
                'away_total_rebounds': 'total_rebounds',
                'away_assists': 'assists',
                'away_steals': 'steals',
                'away_blocks': 'blocks',
                'away_turnovers': 'turnovers',
                'away_fouls': 'fouls'
            })

        final_df = pd.concat([home_df, away_df]).sort_index()
        

        columns_to_average = ['points', 'field_goals', 'field_goal_attempts', 'three_pointers', 'three_point_attempts', 'free_throws', 'free_throw_attempts',
                            'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'fouls',
                            'opp_points', 'opp_field_goals', 'opp_field_goal_attempts', 'opp_three_pointers', 'opp_three_point_attempts', 'opp_free_throws', 'opp_free_throw_attempts',
                            'opp_offensive_rebounds', 'opp_defensive_rebounds', 'opp_total_rebounds', 'opp_assists', 'opp_steals', 'opp_blocks', 'opp_turnovers', 'opp_fouls']
        
        final_df[columns_to_average] = final_df[columns_to_average].astype('float').rolling(window=n_days).mean().dropna()

        final_df[['spread', 'over_under']] = final_df[['spread', 'over_under']].astype('float')

        final_df[['team', 'opp_team']] = final_df[['team', 'opp_team']].astype('int')

        team_dataframes.append(final_df)

    clean_df = pd.concat(team_dataframes)

    #clean_df = clean_df.drop_duplicates(subset=['boxscore'], keep='first')

    return clean_df

def get_todays_games():

    today = date.today()

    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()
        sql_statement = f"""
        SELECT
            boxscores.id,
            boxscores.home_team,
            boxscores.away_team,
            odds.OU
        FROM boxscores
        JOIN dates on dates.id = boxscores.game_date
        JOIN odds on odds.boxscore = boxscores.id
        WHERE dates.game_date = '{today}'
        """
        cursor.execute(sql_statement)
        results = cursor.fetchall()

        return results

def update_bets_table(model_id, money_bet, line, bet_type, winner, gain_loss):
    pass
####################################### Functions for developmental purposes only
#Get the date_id based on a season and mm-dd
def get_date_id(season, mm_dd):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        sql_statement = """
        SELECT id
        FROM dates
        WHERE strftime('%m-%d', game_date) = '{}'
        AND season = {};
        """.format(mm_dd, season)

        cursor.execute(sql_statement)
        game_id = cursor.fetchone()[0]

        return game_id   

def get_team_id(team_name):
        with sql.connect('nba.db') as conn:
            cursor = conn.cursor()

            sql_statement = """
            SELECT id
            FROM teams
            WHERE team_name = '{}';
            """.format(team_name)

            cursor.execute(sql_statement)
            name_id = cursor.fetchone()[0]

            return name_id
        
def get_boxscore_id(date_id, away_team_id, home_team_id):
    with sql.connect('nba.db') as conn:
            cursor = conn.cursor()

            sql_statement = """
            SELECT id
            FROM boxscores
            WHERE home_team = {}
            AND away_team = {}
            AND game_date = {};
            """.format(home_team_id, away_team_id, date_id)

            cursor.execute(sql_statement)
            boxscore_id = cursor.fetchone()[0]

            return boxscore_id
    
def add_to_odds_table(boxscore, ou, homeline):
    with sql.connect('nba.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM odds WHERE boxscore = ?", (boxscore,))
        result = cursor.fetchone()

        if not result:
            cursor.execute('INSERT INTO odds (boxscore, OU, homeline) VALUES (?, ?, ?)', (boxscore, ou, homeline))

        
        conn.commit()