import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
import sql_write_commands as sql
import time

#We want to get season stats from the 2015 season on

#basketball-reference.com/leagues/NBA_YEAR_games-MONTH.html
#We can get boxscore link by scraping all elements of each table for that month and the td: "data-stat='box_score_text" is the element we want
def get_boxscores_year(year, end_year, database='NBA'):
    """
    Extract the boxscore ids for each game starting with a certain year 
    Seasons

    Input:
    year (int): The year you wish the scraping to start from

    Output:
    Writes each box score to a MySQL Database
    """

    months = ['october','november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september']

    for year in range(year, end_year + 1, 1):

        #Add season to database if not currently in it.
        sql.add_season_to_table(year, database=database)

        for month in months:

            url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"

            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            
            time.sleep(3)

            soup = bs(response.content.decode('utf-8'), 'html.parser')

            elements = soup.find_all('td', {'data-stat': 'box_score_text'})

            for element in elements:
                # Create the ability to access and data within that row

                row = element.find_parent('tr')

                # Extract visitor-team-name and home-team-name within the row
                visitor_name = row.find('td', {'data-stat': 'visitor_team_name'}).text.strip()
                home_name = row.find('td', {'data-stat': 'home_team_name'}).text.strip()

                # Extract Boxscore
                try:
                    boxscore = element.find('a').get('href')
                except AttributeError as e:
                    print("Boxscores scraped")
                    break
                #Parse boxscore for date
                date_string = boxscore[11:19]
                date = datetime.strptime(date_string, '%Y%m%d').date()

                #If date is not in database, add it
                sql.add_date_to_table(date, year, database=database)

                # Write to sqllite database
                sql.add_boxscore_to_table(date, home_name, visitor_name, boxscore, database=database)

def populate_game_stats(boxscore_id, url, MAX_RETRIES=10, database='NBA'):

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
    
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get('http://'+url, headers=headers, timeout=10)
            break
        except requests.exceptions.RequestException as e:
            print(f"Request Error {e}, Retry attempt {_}...")
            time.sleep(3)

    time.sleep(3)
    
    if response.status_code != 200:
        print(f"TIMED OUT AFTER {MAX_RETRIES}, PAUSING FOR 60 SECONDS THEN REATTEMPTING")
        time.sleep(60)
        #Recursion
        populate_game_stats(boxscore_id, url)

    else:
        soup = bs(response.content.decode('utf-8'), 'html.parser')

        tables = soup.find_all('table', {'class': ['sortable', 'stats_table', 'now_sortable']})

        for table in tables:
            caption = table.find('caption').text[-30:]
            if caption == 'Basic and Advanced Stats Table':
                team_id = sql.retrieve_team_information(table.find('caption').text[0:-31], database=database)[0]
                #Find the team Totals row
                team_stats = table.find(text="Team Totals").find_parent().find_parent()
                #Add stats to team
                #Field Goals
                field_goals = int(team_stats.find('td', {'data-stat': 'fg'}).text.strip())
                #Field Goals Attempted
                field_goal_attempts = int(team_stats.find('td', {'data-stat': 'fga'}).text.strip())
                #Three Pointers
                threes = int(team_stats.find('td', {'data-stat': 'fg3'}).text.strip())
                #Three Point Attempts
                three_point_attempts = int(team_stats.find('td', {'data-stat': 'fg3a'}).text.strip())
                #Free Throws
                free_throws = int(team_stats.find('td', {'data-stat': 'ft'}).text.strip())
                #Free Throw Attempts
                free_throw_attempts = int(team_stats.find('td', {'data-stat': 'fta'}).text.strip())
                #Offensive Rebounds
                offensive_rebounds = int(team_stats.find('td', {'data-stat': 'orb'}).text.strip())
                #Defensive Rebounds
                defensive_rebounds = int(team_stats.find('td', {'data-stat': 'drb'}).text.strip())
                #Total Rebounds
                total_rebounds = int(team_stats.find('td', {'data-stat': 'trb'}).text.strip())
                #Assists
                assists = int(team_stats.find('td', {'data-stat': 'ast'}).text.strip())
                #Steals
                steals = int(team_stats.find('td', {'data-stat': 'stl'}).text.strip())
                #Blocks
                blocks = int(team_stats.find('td', {'data-stat': 'blk'}).text.strip())
                #Turnovers
                turnovers = int(team_stats.find('td', {'data-stat': 'tov'}).text.strip())
                #Personal Fouls
                personal_fouls = int(team_stats.find('td', {'data-stat': 'pf'}).text.strip())
                #Points
                points = int(team_stats.find('td', {'data-stat': 'pts'}).text.strip())

                sql.add_team_stat_information(team_id, boxscore_id, field_goals, field_goal_attempts, 
                                            threes, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds, 
                                            defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, 
                                            personal_fouls, points, database=database)


                tbody = table.find('tbody')
                rows = tbody.find_all('tr')
                for row in rows:
                    player_info = row.find('th')
                    row_class = row.get('class')

                    #Skips the Reserves Portion
                    if row_class:
                        continue

                    player_url = 'https://www.basketball-reference.com' + player_info.find('a').get('href')
                    #Scrape Player Data
                    player = extract_player_information(player_url)
                    #If player does not exist, create player and ID -> otherwise grab ID
                    #Need to add something here! Sometimes NONETYPE object is not subscriptable comes up
                    player_id = sql.retrieve_player_information(player['first_name'], player['middle_name'], player['last_name'], player['birthdate'], database=database)[0]

                    #Check to see if player played, can add everything as 0's
                    no_playtime = row.find('td', {'data-stat': 'reason'})
                    if no_playtime:
                        minutes_played, field_goals, field_goal_attempts = [0] * 3
                        free_throws, free_throw_attempts, threes, three_attempts = [0] * 4
                        offensive_rebounds, defensive_rebounds, total_rebounds = [0] * 3
                        assists, steals, blocks, turnovers, personal_fouls, points = [0] * 6
                    else:
                        #Minutes Played
                        minutes_played = row.find('td', {'data-stat': 'mp'})
                        minutes, seconds = map(int, minutes_played.text.strip().split(":"))
                        minutes_played = round(minutes + seconds/60,2)
                        #Field Goals
                        field_goals = int(row.find('td', {'data-stat': 'fg'}).text.strip())
                        #Field Goals Attempted
                        field_goal_attempts = int(row.find('td', {'data-stat': 'fga'}).text.strip())
                        #Three Pointers
                        threes = int(row.find('td', {'data-stat': 'fg3'}).text.strip())
                        #Three Point Attempts
                        three_point_attempts = int(row.find('td', {'data-stat': 'fg3a'}).text.strip())
                        #Free Throws
                        free_throws = int(row.find('td', {'data-stat': 'ft'}).text.strip())
                        #Free Throw Attempts
                        free_throw_attempts = int(row.find('td', {'data-stat': 'fta'}).text.strip())
                        #Offensive Rebounds
                        offensive_rebounds = int(row.find('td', {'data-stat': 'orb'}).text.strip())
                        #Defensive Rebounds
                        defensive_rebounds = int(row.find('td', {'data-stat': 'drb'}).text.strip())
                        #Total Rebounds
                        total_rebounds = int(row.find('td', {'data-stat': 'trb'}).text.strip())
                        #Assists
                        assists = int(row.find('td', {'data-stat': 'ast'}).text.strip())
                        #Steals
                        steals = int(row.find('td', {'data-stat': 'stl'}).text.strip())
                        #Blocks
                        blocks = int(row.find('td', {'data-stat': 'blk'}).text.strip())
                        #Turnovers
                        turnovers = int(row.find('td', {'data-stat': 'tov'}).text.strip())
                        #Personal Fouls
                        personal_fouls = int(row.find('td', {'data-stat': 'pf'}).text.strip())
                        #Points
                        points = int(row.find('td', {'data-stat': 'pts'}).text.strip())

                    #Add these stats to the table
                    sql.add_player_stat_information(player_id, team_id, boxscore_id, minutes_played, field_goals, field_goal_attempts,
                                                    threes, three_point_attempts, free_throws, free_throw_attempts, offensive_rebounds,
                                                    defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
                                                    personal_fouls, points, database=database)

def extract_player_information(url, MAX_RETRIES=10):

    headers = {
            'User-Agent': 'Chrome'
            }

    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as error:
            print(f"Timed Out, Retry attempt {_}...")
            time.sleep(60)

    time.sleep(3)

    if response.status_code != 200:
        print(f"TIMED OUT AFTER {MAX_RETRIES}, PAUSING FOR 60 SECONDS THEN REATTEMPTING")
        time.sleep(60)
        extract_player_information(url)
        return

    else:
        soup = bs(response.content.decode('utf-8'), 'html.parser')

        player_info = soup.find('div', {'class': 'players'})

        for item in player_info.find_all('strong'):
            if item.parent and item.parent.name == 'strong':
                player_name = item.text.split()
                first_name = player_name[0]
                if player_name[-1] == 'Jr.' or player_name == 'Sr.' or player_name == 'II' or player_name == 'III' or player_name == 'IV':
                    last_name = " ".join(player_name[-2:])
                    middle_name = " ".join(player_name[1:-2])
                else:
                    last_name = player_name[-1]
                    middle_name = " ".join(player_name[1:-1])

        birth_info = player_info.find('span', {'id': 'necro-birth'})
        birthdate =  birth_info['data-birth']

        try:
            return {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, 'birthdate': birthdate}
        
        except UnboundLocalError:
            print("UnboundLocalError in scaping player information for URL: " + url)
            return extract_player_information(url)
        

######################################################################## For testing if all data is present within alloted timeframe!
