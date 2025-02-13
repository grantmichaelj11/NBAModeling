import mysql.connector as sql

def create_database():

    conn = sql.connect(host='localhost',
                    user='root',
                    password='REcon.14',
                    charset='utf8',
                    init_command='SET NAMES UTF8') 
        
    return conn

def connect_to_database(db='NBA'):
    
    conn = sql.connect(host='localhost',
                       user='root',
                       password='REcon.14',
                       database=db,
                       charset='utf8',
                       init_command='SET NAMES UTF8') 
        
    return conn