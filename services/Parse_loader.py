from utills import db_utills, db_load







# load_place=all вернет все типы башен
# load_place={tower_name} вернет записи по башне {tower_name}

def load_results(load_place):
    db_utills.init_db()
    parameters = db_utills.init_params()
    parameters['load_place'] = load_place
    db_load.load_results(parameters)