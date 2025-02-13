import os
import sys
import requests
import pandas as pd
from datetime import datetime

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parentDirectory)
import db_connection as connect

def retrieve_stats_from_player(first_name, last_name, middle_name=None, days=3):

    if middle_name == None:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_career_listed/first_name={first_name}/last_name={last_name}')
    else:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_career_listed/first_name={first_name}/last_name={last_name}/middle_name={middle_name}')

    data = apiinfo.json()

    df = pd.DataFrame.from_dict(data, orient='index')

    columns_to_select = ['Minutes',
                         'Field Goals',
                         'Field Goal Attempts',
                         'Three Pointers',
                         'Three Point Attempts',
                         'Free Throws',
                         'Free Throw Attempts',
                         'Offensive Rebounds',
                         'Defensive Rebounds',
                         'Total Rebounds',
                         'Assists',
                         'Steals',
                         'Blocks',
                         'Turnovers',
                         'Fouls',
                         'Points']

    #N day moving average for player
    for col in columns_to_select:
        df[f'Average {col}'] = df[col].rolling(window=days).mean()

    #Shifts average columns down one so that the current game is not averaged into the results
    for col in columns_to_select:
        df[f'Average {col}'] = df[f'Average {col}'].shift(1)

    df = df.dropna()

    return df.reset_index(drop=True)


def get_team_stats_against_player(player_df, days=3):

    collected_stats = {}

    for i in range(len(player_df)):

        game_data = player_df.iloc[i]
        date = game_data['Game Date']
        opponent = game_data['Opponent']
        apiinfo = requests.get(f'http://127.0.0.1:5000/get_previous_n_team_stats/team_name={opponent}/date={date}/days={days}')

        data = apiinfo.json()

        df = pd.DataFrame.from_dict(data, orient='index')

        if len(df) < days:
            continue

        columns_to_select = [
        'Opponent Field Goals',
        'Opponent Field Goal Attempts',
        'Opponent Three Pointers',
        'Opponent Three Point Attempts',
        'Opponent Free Throws',
        'Opponent Free Throw Attempts',
        'Opponent Offensive Rebounds',
        'Opponent Defensive Rebounds',
        'Opponent Total Rebounds',
        'Opponent Assists',
        'Opponent Steals',
        'Opponent Blocks',
        'Opponent Turnovers',
        'Opponent Fouls',
        'Opponent Points']

        averages = df[columns_to_select].mean()

        averages = averages.to_dict()

        averages['Opponent'] = opponent
        averages['Game Date'] = date

        collected_stats[i] = averages

    df = pd.DataFrame.from_dict(collected_stats, orient='index')

    return df.reset_index(drop=True)


def create_df_for_player(first_name, last_name, middle_name=None, days=3):
    player_stats = retrieve_stats_from_player(first_name, last_name, middle_name, days=days)

    opponent_stats = get_team_stats_against_player(player_stats, days=days)

    final_df = pd.merge(player_stats, opponent_stats, on=['Game Date', 'Opponent'])

    
    #final_df.to_csv(f"{first_name}_{last_name}_{days}.csv", index=False)

    return final_df


def create_player_list_points(database='NBA'):

    with connect.connect_to_database(database) as conn:
        
        cursor = conn.cursor()

        sql_statement = """ SELECT
                                seasons.year as season,
                                AVG(player_stats.points) as avg_points,
                                players.first_name,
                                players.last_name
                            FROM player_stats
                                LEFT JOIN boxscores on player_stats.boxscore=boxscores.id
                                LEFT JOIN dates on boxscores.game_date=dates.id
                                LEFT JOIN seasons on dates.season=seasons.id
                                LEFT JOIN players on player_stats.player=players.id
                            WHERE seasons.year=2025
                            GROUP BY players.first_name, players.last_name
                            HAVING avg_points > 15
                            ORDER BY avg_points DESC;
                        """

        cursor.execute(sql_statement)

        result = cursor.fetchall()

        data = {'First_Name': [], 'Last_Name': []}

        for i in range(len(result)):
            data['First_Name'].append(result[i][2])
            data['Last_Name'].append(result[i][3])

        return pd.DataFrame(data)

#players  = create_player_list_points()

#for i in range(len(players)):
#    first_name, last_name = players.iloc[i].values
#    create_csv_for_player(first_name, last_name)

#create_csv_for_player('Lebron', 'James', days=14)