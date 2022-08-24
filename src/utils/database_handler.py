import psycopg2

import os
#ilgili dosyanın abs pathı bulmak için 3 satır kod
# scrpt_path = path.abspath(__file__)
# dirpath = path.dirname(scrpt_path)
# wordpath = path.join(dirpath, 'words.db')

#heroku .envden db bilgileri
DATABASE_URL = os.getenv("DATABASE_URL")
#######################################EN_TR_WORDS_DB#######################################
def get_words():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM engtrwords LIMIT 150;               
    """)
    result_list = cursor.fetchall()
    conn.close()
    return result_list
def add_new_word(engw,trw):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO engtrwords ("English", "Turkish") VALUES
    (%s, %s)               
    """, (engw, trw))
    conn.commit()
    conn.close()
def delete_word(engw,trw):#buna kondisyon ile kontrol etmemiz gerek ve ona göre kullanıcı bilgilendir
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM engtrwords WHERE "English" = %s and "Turkish" = %s;               
    """,(engw, trw))
    conn.commit()
    conn.close()
############################################################################################
#######################################VERBS_DB#######################################
def get_verbs(tablename:str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {tablename} LIMIT 150;')
    result_lst = cursor.fetchall()
    conn.close()
    return result_lst
######################################################################################
