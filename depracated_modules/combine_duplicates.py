import sqlite3 as lite

with lite.connect('nba.db') as conn:
    #How many players have the same first name and birthday?
    cursor = conn.cursor()

    # cursor.execute('SELECT last_name, birthday FROM players WHERE last_name = ? GROUP BY middle_name, last_name, birthday HAVING COUNT(*) > 1', ('Maledon',))
    # duplicates = cursor.fetchall()
    # print(duplicates)

    # #Can we update the sqlite database to replace player stats with the first properly formatted name?
    # for duplicate in duplicates:
    #     cursor.execute('SELECT * FROM players WHERE last_name = ? and birthday = ?', (duplicate[0], duplicate[1]))
    #     player_id = cursor.fetchall()
    #     id_to_keep, id_to_replace = player_id[0][0], player_id[1][0]

    #     #Then can we update the sqlite database to eliminate the duplicate players from the db
    #     cursor.execute(f'UPDATE player_stats SET player = {id_to_keep} WHERE player = {id_to_replace}')
    #     cursor.execute(f'DELETE FROM players WHERE id = {id_to_replace}')

    #     conn.commit()

    # #Then can we update the sqlite database to eliminate the duplicate players from the db

    id_to_keep, id_to_replace = 585, 1436 

    cursor.execute(f'UPDATE player_stats SET player = {id_to_keep} WHERE player = {id_to_replace}')
    cursor.execute(f'DELETE FROM players WHERE id = {id_to_replace}')

    conn.commit()

