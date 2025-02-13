import sql_write_commands as sql
from bs4 import BeautifulSoup as bs
import db_connection as connect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import time

def search_player_name(first_name, last_name, middle_name=None):

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.basketball-reference.com/')

    time.sleep(3)

    search_box = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[3]/form/div/div/input[2]')
    submit_button = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[3]/form/input[1]')

    if middle_name == None:
        middle_name = ""

    if last_name == 'Sr.' or last_name == 'II' or last_name == 'III' or last_name == 'IV':
        search_box.send_keys(f'{first_name} {middle_name}')

    else:
        search_box.send_keys(f'{first_name} {middle_name} {last_name}')

    submit_button.click()

    time.sleep(3)

    try:
        player_link = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/strong/a')
    except selenium.common.exceptions.NoSuchElementException:
        player_link = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/a')

    player_link.click()

    time.sleep(3)
    soup = bs(driver.page_source, 'html.parser')
    player_info = soup.find('div', {'class': 'players'})

    for item in player_info.find_all('strong'):
        if item.parent and item.parent.name == 'strong':
            player_name = item.text.split()
            first_name = player_name[0]
            if player_name[-1] == 'Jr.' or player_name[-1] == 'Sr.' or player_name[-1] == 'II' or player_name[-1] == 'III' or player_name[-1] == 'IV':
                last_name = " ".join(player_name[-2:])
                middle_name = " ".join(player_name[1:-2])
            else:
                last_name = player_name[-1]
                middle_name = " ".join(player_name[1:-1])

    print(last_name)

    driver.close()

    return first_name, middle_name, last_name

def get_all_players():

    with connect.connect_to_database() as conn:
        cursor = conn.cursor()

        sql_statement = f'SELECT * FROM players'
        cursor.execute(sql_statement)
        result = cursor.fetchall()

    return result

def update_players_table(first_name, last_name, middle_name=None):
    

    updated_name = search_player_name(first_name, last_name, middle_name)

    with connect.connect_to_database() as conn:
        cursor = conn.cursor()

        sql_statement = '''
        UPDATE players 
        SET first_name = %s, middle_name = %s, last_name = %s 
        WHERE first_name = %s AND middle_name = %s AND last_name = %s;
        '''

        params = (updated_name[0], updated_name[1], updated_name[2], first_name, middle_name, last_name)

        cursor.execute(sql_statement, params)

        conn.commit()

for player in get_all_players():    
    first_name, last_name, middle_name = player[1], player[2], player[3]
    test_name = last_name.split()
    if len(test_name) > 1:
        if test_name[0] == test_name[1]:
            update_players_table(first_name, last_name, middle_name)
    else:
        if last_name == 'Sr.' or last_name == 'II' or last_name == 'III' or last_name == 'IV':
            update_players_table(first_name, last_name, middle_name)



