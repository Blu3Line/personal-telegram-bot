import psycopg2

from src.objects import DB_URI
#ilgili dosyanın abs pathı bulmak için 3 satır kod
# scrpt_path = path.abspath(__file__)
# dirpath = path.dirname(scrpt_path)
# wordpath = path.join(dirpath, 'words.db')

#heroku .envden db bilgileri

def db_verify(connection, cursor) -> bool:  # FIXME: asyncio ile bir şeyler eklenebilir mi?
    # TODO:script mainden çalıştırılırken sadece 1 kere çalışsın (program başlangıcı check)
    # TODO:log sistemini uygula
    print("\nVeritabanı doğrulaması başlıyor...")
    try:
        cursor.execute(open("db-verify.sql", "r").read())
        cursor.execute("select * from user_acces_level")
        if len(cursor.fetchall()) != 3:
            cursor.executemany("INSERT INTO user_acces_level VALUES (%s, %s)",
                               [(1, "pleb"), (2, "admin"), (3, "owner")])


    except psycopg2.errors.UniqueViolation as e:
        print("user_acces_level dosyasındaki entityler sıkıntılı:", e)
    except FileNotFoundError as e:
        print("script dosyasına erişim yapılamadı:", e)
    except Exception as e:
        print("Beklenmedik sorun oluştu!", e)
    else:
        connection.commit()
        print("Database doğrulaması tamamlandı!\n")
        return

    # FAIL AND EXIT PART
    connection.close()  # işlem tamamlanamadı database kapatıcak ve programı kapat(#TODO:main programa göre editle burayı)
    print("Database doğrulaması başarısız!\n")
    exit()



#######################################EN_TR_WORDS_DB#######################################
def get_words():
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM engtrwords LIMIT 150;               
    """)
    result_list = cursor.fetchall()
    conn.close()
    return result_list

def find_word(word):
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM engtrwords WHERE "English" = %s or "Turkish" = %s;               
    """,(word,word))
    result_list = cursor.fetchall()
    conn.close()
    return result_list
def add_new_word(engw,trw):
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO engtrwords ("English", "Turkish") VALUES
    (%s, %s)               
    """, (engw, trw))
    conn.commit()
    conn.close()
def delete_word(engw,trw):#buna kondisyon ile kontrol etmemiz gerek ve ona göre kullanıcı bilgilendir
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM engtrwords WHERE "English" = %s and "Turkish" = %s;               
    """,(engw, trw))
    conn.commit()
    conn.close()
############################################################################################
#######################################VERBS_DB#######################################
def get_verbs(tablename:str):
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {tablename} LIMIT 150;')
    result_lst = cursor.fetchall()
    conn.close()
    return result_lst
######################################################################################
#TODO
#dbden istenilen şey olmazsa diye ona göre respond atabilmeli 