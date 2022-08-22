import sqlite3
#ilgili dosyanın abs pathı bulmak için 3 satır kod
# scrpt_path = path.abspath(__file__)
# dirpath = path.dirname(scrpt_path)
# wordpath = path.join(dirpath, 'words.db')

def connect_db():
    conn = sqlite3.connect("bot_database.sqlite")
    cursor = conn.cursor()
    
    return conn, cursor

def read_db(cursor, table_name:str):
    cursor.execute(
        """SELECT * FROM %s;""", (table_name,))
    return cursor.fetchall()


