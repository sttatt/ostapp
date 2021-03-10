import os
import regex as re
import pymorphy2, datetime
import pandas as pd
from utills import db_utills
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import pdist, squareform

morph = pymorphy2.MorphAnalyzer()

def get_stop_words():
    query_res = db_utills.select_query("SELECT name FROM stop_words")
    stopwords = []
    for word in query_res:
        stopwords.append(str(word.__getitem__(0)))
    return stopwords

def normalize(text):
    tokens = re.findall('[A-Za-zA-Яа-яЁё]+\-[A-Za-zA-Яа-яЁё]+|[[A-Za-zA-Яа-яЁё]+', text)
    user_stopwords = get_stop_words()
    words = []
    for word in tokens:
        pv = morph.parse(word)
        if pv[0].normal_form not in stopwords.words('russian') and pv[0].normal_form not in user_stopwords:
            words.append(pv[0].normal_form)
    return words


def contains_morph(phrase, morphology):
    for word in phrase.split(' '):
        if morph.parse(word)[0].tag.POS == morphology:
            return True


def check_phrase(phrase):
    if contains_morph(phrase, 'INFN') and (contains_morph(phrase, 'ADVB')):
        return True
    elif contains_morph(phrase, 'NOUN') and (contains_morph(phrase, 'ADJF')):
        return True
    else:
        return False


def get_check_tf_idf(df):
    for i, phrase in enumerate(df.index):
        if check_phrase(phrase):
            continue
        else:
            df.drop(phrase, inplace=True)
    return df


def get_result_tf_idf_for_tower(tf_result, tfCounter,
                                df_tower):  # Получение итоговых данных по tf-idf  и матрицы для расчета cos
    tower_dataframe = pd.DataFrame(tf_result.todense(), columns=tfCounter.get_feature_names())
    tower_dataframe = get_check_tf_idf(tower_dataframe.T)
    tower_docs_for_cos = tower_dataframe
    tower_dataframe = tower_dataframe.T.join([df_tower['date'], df_tower['place']])
    list_of_groups = []
    for name, group in tower_dataframe.groupby('date'):
        group_median = pd.DataFrame(group.median())
        group_median.columns = ['median']
        group_res = pd.DataFrame(group.describe().T.join(group_median))
        del group_res['std']
        del group_res['min']
        del group_res['count']
        group_res['date'] = name
        group_res['place'] = df_tower['place'][0]
        list_of_groups.append(group_res)
    tower_dataframe = pd.concat([res for res in list_of_groups])
    tower_dataframe = tower_dataframe.reset_index()
    tower_dataframe.columns = ['words', 'mean', 'qw_25%', 'qw_50%', 'qw_75%', 'max', 'median', 'date', 'place']
    return tower_dataframe, tower_docs_for_cos


def get_cosine_matrix(tower_docs_for_cos, tower_docs):
    res = pd.DataFrame(squareform(pdist(tower_docs_for_cos, metric='cosine')),
                       columns=[w for w in tower_docs_for_cos.index])
    res.index = [w for w in tower_docs_for_cos.index]
    res_list = []
    for n in res:
        for j in res[n]:
            if j >= 0.55:
                continue
            else:
                for index in res.loc[res[n] == j].index:
                    string = [j, n, index]
                    res_list.append(string)
    cos_matr = pd.DataFrame(res_list, columns=['cosine', 'word_1', 'word_2'])
    cos_matr['place'] = tower_docs['place'][0]
    return cos_matr


def get_result(df_tower):
    tfCounter = TfidfVectorizer(ngram_range=(2, 2),
                                token_pattern=r'[A-Za-zA-Яа-яЁё]+\-[A-Za-zA-Яа-яЁё]+|[[A-Za-zA-Яа-яЁё]+')
    tf_result = tfCounter.fit_transform([' '.join(normalize(otz)) for otz in df_tower.text])
    tower_docs, tower_docs_for_cos = get_result_tf_idf_for_tower(tf_result, tfCounter, df_tower)
    cos_matrix = get_cosine_matrix(tower_docs_for_cos, tower_docs)
    tower_docs = tower_docs.query('mean != 0 and max != 0')
    return tower_docs, cos_matrix


def save_results(tower_docs, cos_matrix):  # Сохранение итоговых датафреймов
    try:
        os.makedirs("analyse_result/history/"+SESSION_ID+"/", exist_ok=True)
        os.makedirs("analyse_result/current_result/", exist_ok=True)
    except OSError:
        print('load results directory create error')
    tower_docs.to_csv("analyse_result/history/"+SESSION_ID+"/tf_idf_words.csv")
    tower_docs.to_csv("analyse_result/current_result/tf_idf_words.csv")
    cos_matrix.to_csv("analyse_result/history/"+SESSION_ID+"/cos_matrix.csv")
    cos_matrix.to_csv("analyse_result/current_result/cos_matrix.csv")

    db_load


def start():
    print("begin algorithm")
    global SESSION_ID
    SESSION_ID = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file = pd.read_json(db_utills.get_param("current_load_directory")+"result.json", encoding='utf-8')
    print(file.__len__())
    tf_idf_words, cos_matrix = get_result(file)
    save_results(tf_idf_words, cos_matrix)

# save_results(berlin_tf_idf_words, berlin_cos_matrix)
#
# burj_al_arab = pd.read_json('burj_al_arab.json', encoding='utf-8')
# burj_al_arab_tf_idf_words, burj_al_arab_cos_matrix = get_result(burj_al_arab)
# save_results(burj_al_arab_tf_idf_words, burj_al_arab_cos_matrix)
#
# canton_tower = pd.read_json('canton_tower.json', encoding='utf-8')
# canton_tower_tf_idf_words, canton_tower_cos_matrix = get_result(canton_tower)
# save_results(canton_tower_tf_idf_words, canton_tower_cos_matrix)
#
# chicago_360 = pd.read_json('chicago_360.json', encoding='utf-8')
# chicago_360_tf_idf_words, chicago_360_cos_matrix = get_result(chicago_360)
# save_results(chicago_360_tf_idf_words, chicago_360_cos_matrix)
#
# eifel_tower = pd.read_json('eifel_tower.json', encoding='utf-8')
# eifel_tower_tf_idf_words, eifel_tower_cos_matrix = get_result(eifel_tower)
# save_results(eifel_tower_tf_idf_words, eifel_tower_cos_matrix)
#
# empire_state_building = pd.read_json('empire_state_building.json', encoding='utf-8')
# empire_state_building_tf_idf_words, empire_state_building_cos_matrix = get_result(empire_state_building)
# save_results(empire_state_building_tf_idf_words, empire_state_building_cos_matrix)
#
# sidney_tower = pd.read_json('eifel_tower.json', encoding='utf-8')
# sidney_tower_tf_idf_words, sidney_tower_cos_matrix = get_result(sidney_tower)
# save_results(sidney_tower_tf_idf_words, sidney_tower_cos_matrix)
#
# tai_pei_tower = pd.read_json('tai_pei_tower.json', encoding='utf-8')
# tai_pei_tower_tf_idf_words, tai_pei_tower_cos_matrix = get_result(tai_pei_tower)
# save_results(tai_pei_tower_tf_idf_words, tai_pei_tower_cos_matrix)
#
# tallin_tower = pd.read_json('tallin_tower.json', encoding='utf-8')
# tallin_tower_tf_idf_words, tallin_tower_cos_matrix = get_result(tallin_tower)
# save_results(tallin_tower_tf_idf_words, tallin_tower_cos_matrix)
#
# tokio_tower = pd.read_json('tokio_tower.json', encoding='utf-8')
# tokio_tower_tf_idf_words, tokio_tower_cos_matrix = get_result(tokio_tower)
# save_results(tokio_tower_tf_idf_words, tokio_tower_cos_matrix)
#
# torre_latino_tower = pd.read_json('torre_latino_tower.json', encoding='utf-8')
# torre_latino_tower_tf_idf_words, torre_latino_tower_cos_matrix = get_result(torre_latino_tower)
# save_results(torre_latino_tower_tf_idf_words, torre_latino_tower_cos_matrix)
#
# ostankino_tower = pd.read_json('ostankino_tower.json', encoding='utf-8')
# ostankino_tower_tf_idf_words, ostankino_tower_cos_matrix = get_result(ostankino_tower)
# save_results(ostankino_tower_tf_idf_words, ostankino_tower_cos_matrix)
#
