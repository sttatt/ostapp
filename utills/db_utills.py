import sqlite3, datetime, traceback

ERROR="ERROR"
OK = "OK"
DB_NAME='project_db.db'

def multiply_insert(columns, rows, table_name, session_id):
    res = 'begin'
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        columns.append('session_id')
        columns.append('date_create')
        for row in rows:
            row.append(session_id)
            row.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            query = "insert or ignore INTO %s %s values %s" % (table_name, tuple(columns), tuple(row))
            cursor.execute(query)
            #cursor.execute(query+" "+values)
            # for row in cos_matrix.itertuples():
            #     query = "insert or ignore INTO cos_matrix (cosine, word_1, word_2, place, session_id, date_create) values (%s, '%s', '%s', '%s', %s, DateTime('now'))" % (
            #     float(row.cosine), row.word_1, row.word_2, row.place, parameters['session_id'])
            #     db_utills.update_query(query)

            # tf_idf_words = pandas.read_csv("analyse_result/current_result/tf_idf_words.csv");
            # for row in tf_idf_words.itertuples():
            #     query = "insert or ignore INTO tf_idf_words (words,mean,qw_25,qw_50,qw_75,max,median,date,place, session_id, date_create) " \
            #             "values ('%s', '%s', '%s', '%s', %s, %s, %s, %s, '%s', %s, DateTime('now'))" \
            #             % (row.words, row.mean, row._4, row._5, row._6, row.max, row.median, row.date, row.place, parameters['session_id'])
            #     db_utills.update_query(query)
        connection.commit()
        cursor.close()
        res = OK
    except Exception as error:
        res = "Ошибка sql lite: "+error
        traceback.print_exc()
    finally:
        if(connection):
            connection.close()
        return res



def update_query(query):
    res = ''
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        res = OK
    except Exception as error:
        res = traceback.format_exc(error)
        print("Ошибка sql lite", error)
    finally:
        if(connection):
            connection.close()
        return res

def select_query(query):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        #result = 'result'
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
    except Exception as error:
        print("Ошибка sql lite", error)
        result = error
    finally:
        if(connection):
            connection.close();
        return result

def get_param(param):
    query = "SELECT value FROM parameters where name='%s'" % param
    print(query)
    return select_one_item(query)


def init_db():
    def existence_query(table_name):
        return "SELECT count(name) FROM sqlite_master WHERE type='table' AND UPPER(name)=upper('%s');"% (table_name)
    def create_table(query, table_name):
        try:
            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()
            cursor.execute(existence_query(table_name))
            if (cursor.fetchone()[0] == 0):
                cursor.executescript(query)
                connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Ошибка создания таблицы", error)
        finally:
            if (connection):
                connection.close()
    create_table('''CREATE TABLE sites (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
     name TEXT NOT NULL UNIQUE,
     link TEXT NOT NULL,
     active BOOLEAN DEFAULT TRUE
     );''', 'sites')
    create_table('''CREATE TABLE parameters (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL);
    ''', 'parameters')
    create_table('''CREATE TABLE results (id text NOT NULL,
    text TEXT NOT NULL,
    review_quantity INTEGER, 
    stars INTEGER, 
    date TEXT,
    place TEXT,
    translated boolean,
    converted_date DATE,
    date_create DATE,
    order_type TEXT,
    source TEXT,
    primary key (id, place));''', 'results')
    create_table('''CREATE TABLE stop_words (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         name TEXT NOT NULL UNIQUE,
         active BOOLEAN DEFAULT TRUE
         );''', 'stop_words')
    create_table('''CREATE TABLE cos_matrix (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             cosine FLOAT,
             word_1 TEXT, 
             word_2 TEXT, 
             place TEXT,
             session_id INTEGER,
             date_create date
             );''', 'cos_matrix')
    create_table('''CREATE TABLE tf_idf_words (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             words TEXT,
             mean float ,
             qw_25 float ,
             qw_50 float ,
             qw_75 float,
             max float,
             median float,
             date date,
             place text,
             session_id INTEGER,
             date_create date
             );''', 'tf_idf_words')
    create_table('''CREATE TABLE parse_sessions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            session_id INTEGER,
            date_create date,
            status TEXT
    )''', "parse_sessions")
    create_table('''CREATE TABLE analyse_sessions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                session_id INTEGER,
                date_create date,
                status TEXT
        )''', "analyse_sessions")




    #init params
    update_query("insert or ignore into parameters (name, value) values ('results_directory', 'results/');")
    update_query("insert or ignore into parameters (name, value) values ('no_trans_directory', 'no_trans_results/');")
    update_query("insert or ignore into parameters (name, value) values ('current_load_directory', 'loads/current_load/');")
    update_query("insert or ignore into parameters (name, value) values ('load_history_directory', 'loads/load_history/');")
    update_query("insert or ignore into parameters (name, value) values ('webdriver_abs_path', 'D:/chromedriver_win32/chromedriver.exe');")
    update_query("insert or ignore into parameters (name, value) values ('test', '0');")
    update_query("insert or ignore into parameters (name, value) values ('timeout', '5');")
    update_query("insert or ignore into parameters (name, value) values ('load_place', 'tokio_tower');")

    #init stop_words
    update_query("insert or ignore INTO stop_words ('name') values ('очень');")
    update_query("insert or ignore INTO stop_words ('name') values ('весь');")
    update_query("insert or ignore INTO stop_words ('name') values ('место');")
    update_query("insert or ignore INTO stop_words ('name') values ('точка');")
    update_query("insert or ignore INTO stop_words ('name') values ('вид');")
    update_query("insert or ignore INTO stop_words ('name') values ('высокий');")
    update_query("insert or ignore INTO stop_words ('name') values ('высота');")
    update_query("insert or ignore INTO stop_words ('name') values ('отель');")
    update_query("insert or ignore INTO stop_words ('name') values ('птичий');")
    update_query("insert or ignore INTO stop_words ('name') values ('высоко');")
    update_query("insert or ignore INTO stop_words ('name') values ('открываться');")
    update_query("insert or ignore INTO stop_words ('name') values ('ладонь');")
    update_query("insert or ignore INTO stop_words ('name') values ('супер');")
    update_query("insert or ignore INTO stop_words ('name') values ('полет');")
    update_query("insert or ignore INTO stop_words ('name') values ('полёт');")
    update_query("insert or ignore INTO stop_words ('name') values ('башня');")
    update_query("insert or ignore INTO stop_words ('name') values ('ладонь');")
    update_query("insert or ignore INTO stop_words ('name') values ('стоить');")
    update_query("insert or ignore INTO stop_words ('name') values ('город');")
    update_query("insert or ignore INTO stop_words ('name') values ('телебашня');")
    update_query("insert or ignore INTO stop_words ('name') values ('опыт');")
    update_query("insert or ignore INTO stop_words ('name') values ('быть');")
    update_query("insert or ignore INTO stop_words ('name') values ('любить');")
    update_query("insert or ignore INTO stop_words ('name') values ('посетить');")
    update_query("insert or ignore INTO stop_words ('name') values ('сидней');")
    update_query("insert or ignore INTO stop_words ('name') values ('берлин');")
    update_query("insert or ignore INTO stop_words ('name') values ('увидеть');")
    update_query("insert or ignore INTO stop_words ('name') values ('чикаго');")
    update_query("insert or ignore INTO stop_words ('name') values ('бурдж аль-араб');")
    update_query("insert or ignore INTO stop_words ('name') values ('а-да');")
    update_query("insert or ignore INTO stop_words ('name') values ('гуанчжоу');")
    update_query("insert or ignore INTO stop_words ('name') values ('париж');")
    update_query("insert or ignore INTO stop_words ('name') values ('этаж');")
    update_query("insert or ignore INTO stop_words ('name') values ('сказать');")
    update_query("insert or ignore INTO stop_words ('name') values ('прекрасный');")
    update_query("insert or ignore INTO stop_words ('name') values ('просто');")
    update_query("insert or ignore INTO stop_words ('name') values ('это');")
    update_query("insert or ignore INTO stop_words ('name') values ('то');")
    update_query("insert or ignore INTO stop_words ('name') values ('burj al arab');")
    update_query("insert or ignore INTO stop_words ('name') values ('burj al');")
    update_query("insert or ignore INTO stop_words ('name') values ('бурдж');")
    update_query("insert or ignore INTO stop_words ('name') values ('аль-араб');")
    update_query("insert or ignore INTO stop_words ('name') values ('арабский');")
    update_query("insert or ignore INTO stop_words ('name') values ('объединить');")
    update_query("insert or ignore INTO stop_words ('name') values ('дубай');")
    update_query("insert or ignore INTO stop_words ('name') values ('эмират');")
    update_query("insert or ignore INTO stop_words ('name') values ('burj');")
    update_query("insert or ignore INTO stop_words ('name') values ('al');")
    update_query("insert or ignore INTO stop_words ('name') values ('arab');")
    update_query("insert or ignore INTO stop_words ('name') values ('который');")
    update_query("insert or ignore INTO stop_words ('name') values ('идти');")
    update_query("insert or ignore INTO stop_words ('name') values ('должный');")
    update_query("insert or ignore INTO stop_words ('name') values ('посещение');")
    update_query("insert or ignore INTO stop_words ('name') values ('обязательно');")
    update_query("insert or ignore INTO stop_words ('name') values ('эмпаер');")
    update_query("insert or ignore INTO stop_words ('name') values ('эмпаир');")
    update_query("insert or ignore INTO stop_words ('name') values ('эмпайр');")
    update_query("insert or ignore INTO stop_words ('name') values ('стэйт');")
    update_query("insert or ignore INTO stop_words ('name') values ('стейт');")
    update_query("insert or ignore INTO stop_words ('name') values ('билдинг');")
    update_query("insert or ignore INTO stop_words ('name') values ('стейт-билдинг');")
    update_query("insert or ignore INTO stop_words ('name') values ('a');")
    update_query("insert or ignore INTO stop_words ('name') values ('да');")
    update_query("insert or ignore INTO stop_words ('name') values ('а-да тарай');")


    print('database inited')

def select_one_item(query):
    try:
        items = select_query(query)
        return items.__getitem__(0).__getitem__(0)
    except Exception as e:
        traceback.print_exc()
        return 'error'
def init_params():
    return dict(select_query("SELECT name, value FROM parameters"))

    #selenium_parse()
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/