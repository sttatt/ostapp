import json, datetime
from utills import db_utills
import os, csv, pandas, glob

def save_to_db(data):
    print("Сохранение в БД...")
    for item in data:
        update_query = "INSERT INTO results %s values %s;" % (tuple(item.keys()), tuple(item.values()))
        db_utills.update_query(update_query)
        #db_utills.update_query("UPDATE sites SET active=FALSE where name='"+name+"';")
    print("Результат сохранен в БД")

def load_results(parameters):
    try:
        os.makedirs(parameters['current_load_directory'], exist_ok=True)
        os.makedirs(parameters['load_history_directory'], exist_ok=True)
    except OSError:
        print('load results directory create error')
    place = parameters['load_place']
    if place == 'all':
        place_query = ""
    else:
        place_query = "  and place='"+place+"'"
    session_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    rows = ['id', 'text' , 'review_quantity','stars','date','place','translated']
    res = (db_utills.select_query("SELECT id, text, review_quantity, stars, converted_date, place, translated FROM results "
                                  "where text is not null "
                                  "and text !=''"
                                  +place_query))
    json_list = []
    for item in res:
        item = list(item)
        item[4] = item[4][3:]
        json_list.append(dict(zip(rows,item)))

    import pathlib
    current_load_path = parameters['current_load_directory']
    load_history_path = parameters['load_history_directory']
    print(current_load_path)
    print(load_history_path+session_id)
    with open(current_load_path+'result.json','w+',encoding='utf-8') as file:
        json.dump(json_list, file, indent=3, ensure_ascii=False)
    with open(load_history_path+session_id+'_result.json','w+',encoding='utf-8') as file:
        json.dump(json_list, file, indent=3, ensure_ascii=False)


def load_analyse_result(session_id):
    for file in glob.glob("analyse_result/current_result/*cos_matrix.csv"):
        cos_matrix = pandas.read_csv(file)
        cos_matrix = cos_matrix.drop(cos_matrix.columns.__getitem__(0), 1)
        rows = cos_matrix.values.tolist()
        columns = cos_matrix.columns.tolist()
        res = db_utills.multiply_insert(columns, rows, 'cos_matrix', session_id)
        if res == "OK":
            print('cos_matrix saved to db')
        else:
            print('cos_matrix result saving error')

    for file in glob.glob("analyse_result/current_result/*tf_idf_words.csv"):
        tf_idf_words = pandas.read_csv(file);
        tf_idf_words = tf_idf_words.drop(tf_idf_words.columns.__getitem__(0), 1)
        rows= tf_idf_words.values.tolist()
        columns = tf_idf_words.columns.tolist()
        for i in range(columns.__len__()):
            columns[i] = columns[i].replace("%", "")
        res = db_utills.multiply_insert(columns, rows, 'tf_idf_words', session_id)
        if res == "OK":
            print('tf_idf_words result saved to db')
        else:
            print('tf_idf_words result saving error')


    # for row in rows:
    #     columns.append('session_id')
    #     columns.append('date_create')
    #     row.append(session_id)
    #     row.append(datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))
    #     print(columns)
    #     print(row)
    #     query = "INSERT INTO %s %s values %s" % (table_name, tuple(columns), tuple(row))
    #     print(query)
    #     #cursor.execute(query)


    #
    # for row in cos_matrix.itertuples():
    #     #print(row)
    #     columns = cos_matrix.columns
    #     query = "INSERT INTO cos_matrix (cosine, word_1, word_2, place, session_id, date_create) values (%s, '%s', '%s', '%s', %s, DateTime('now'))" % (float(row.cosine), row.word_1, row.word_2, row.place, parameters['session_id'])
    #     #db_utills.update_query(query)


    # for row in tf_idf_words.itertuples():
    #     query = "INSERT INTO tf_idf_words (words,mean,qw_25,qw_50,qw_75,max,median,date,place, session_id, date_create) " \
    #             "values ('%s', '%s', '%s', '%s', %s, %s, %s, %s, '%s', %s, DateTime('now'))" \
    #             % (row.words, row.mean, row._4, row._5, row._6, row.max, row.median, row.date, row.place, parameters['session_id'])
    #     db_utills.update_query(query)
