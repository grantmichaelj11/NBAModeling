import db_connection as connect
import numpy as np

def acquire_all_boxscores(database='NBA'):

    with connect.connect_to_database(database) as conn:

        cursor = conn.cursor()

        sql_statement = ''' SELECT * FROM boxscores'''
        cursor.execute(sql_statement)
        result = cursor.fetchall()

        return result
    
def acquire_all_games_team(database='NBA'):

    with connect.connect_to_database(database) as conn:

        cursor = conn.cursor()

        sql_statement = ''' SELECT boxscore FROM team_stats'''
        cursor.execute(sql_statement)
        result = cursor.fetchall()

        return result
    
def ensure_duplicates_for_all_team_stats(team_boxscores):
    #This will ensure that all team stats have both teams who played in the game
    unique_elements, counts = np.unique(team_boxscores, return_counts=True)
    return np.all(counts == 2)

def find_boxscores_not_in_stats(boxscores, stats):

    unique_team_stats = np.unique(stats)
    
    return np.setdiff1d(boxscores, unique_team_stats)

def create_boxscore_array(boxscores):

    boxscore_ids = np.zeros(len(boxscores))
    for i in range(len(boxscores)):
        boxscore_ids[i] = boxscores[i][0]

    return boxscore_ids

boxscores = create_boxscore_array(acquire_all_boxscores())
team_stats = create_boxscore_array(acquire_all_games_team())

if ensure_duplicates_for_all_team_stats(team_stats):
    print("ALL TEAM STATS APPEAR")
else:
    print("MISSING TEAM STATISTICS")

if len(find_boxscores_not_in_stats(boxscores, team_stats)) == 0:
    print('ALL TEAM GAMES ACCOUNTED FOR')
else:
    print("MISSING GAMES")

