from utills import db_utills, result_conversion, parserUtill,db_load
import json
import re
import schedule
import glob, threading
import os, datetime, time
import traceback
import threading



def init_params():
    parameters = db_utills.init_params()
    parameters['no_trans_directory'] = 'parse_results/'+SESSION_ID+'/'+parameters['no_trans_directory']
    parameters['results_directory'] = 'parse_results/'+SESSION_ID+'/'+parameters['results_directory']
    print('parameters inited')
    return parameters

# statuses = (work, done)
def init_session():
    query = "INSERT INTO parse_sessions (session_id, date_create, status) "\
                           "values (%s, '%s', '%s');" % (SESSION_ID, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'work')
    res = db_utills.update_query(query=query)
    print('session inited')
    return res

def init_directories(parameters):
    try:
        os.makedirs(parameters['no_trans_directory'])
        os.makedirs(parameters['results_directory'])
        print('directories inited')
    except OSError as e:
        print(traceback.format_exc())

def  begin_parse(parameters):
    res = db_utills.select_query("SELECT NAME from sites s where s.active=True;")
    for name in res:
        query = "SELECT name, link FROM sites where upper(NAME)=upper('%s')" % name.__getitem__(0)
        site = db_utills.select_query(query)
        name = site.__getitem__(0).__getitem__(0)
        link = site.__getitem__(0).__getitem__(1)
        print("Парсинг: "+name)

        #Если тест, то только один тип сортировки
        if parameters['test'] == '0':
            r = 4
        else:
            r = 1
        #Парсинг для каждого вида сортировки
        for count in range(r):
            result = result_conversion.convert_json(parserUtill.make_parse(name, link, parameters, count))
            db_load.save_to_db(result)
        db_utills.update_query("UPDATE parse_sessions SET STATUS='done' where SESSION_ID=%s" % SESSION_ID)

        print("Парсинг "+name+" закончен")

def test(parameters):
    myset = set()
    path = parameters['results_directory']
    c = 0
    for filename in glob.glob(os.path.join(path, '*.json')):
        c = c+1
        with open(os.path.join(os.getcwd(), filename), 'r', encoding='utf-8') as r_file:
            data = json.load(r_file)
            for item in data:
                date = item['date']
                value = re.sub("\d+", "", date)
                value = value.replace("назад", "")
                value = value.strip()
                myset.add(value)
                print(value)
def start_scheduled_parse(parameters):
    schedule.every(10).seconds.do(begin_parse, parameters)

    while True:
        schedule.run_pending()
        print('done')
        time.sleep(1)

class ParseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global SESSION_ID
        SESSION_ID = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        db_utills.init_db()
        init_session()
        parameters = init_params()
        init_directories(parameters)
        print("---------------")
        print("parsing started")
        try:
            begin_parse(parameters)
        except Exception as e:
            db_utills.update_query("UPDATE parse_sessions SET STATUS='error' where SESSION_ID=%s" % SESSION_ID)
            traceback.print_exc()
        print("parsing finished")
        if (db_utills.select_one_item("SELECT status FROM parse_sessions where session_id=%s" % SESSION_ID)) != 'done':
            db_utills.update_query("UPDATE parse_sessions SET STATUS='error' where SESSION_ID=%s" % SESSION_ID)

def start():

    #start_scheduled_parse(parameters)
    # begin_parse(parameters)


    thread1 = ParseThread()
    thread1.start()