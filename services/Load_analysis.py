from utills import db_load
import datetime



if __name__ == '__main__':
    global SESSION_ID
    SESSION_ID = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    parameters = {}
    parameters['session_id'] = SESSION_ID
    db_load.load_analyse_result(parameters)
    print('123')