import pymorphy2, time, pandas
import re, datetime, csv, glob,  os
from dateutil.relativedelta import relativedelta

from utills import db_utills
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utills import db_load


morph = pymorphy2.MorphAnalyzer()
list1 = ['ехать весело', 'есть мясо', 'вкусное мясо', 'любители мяса', 'люблю гулять']
list3 = ['ехать весело', 'есть мясо', 'вкусное мясо', 'любители мяса', 'люблю гулять']
list2 =[]


def contains_morph(phrase, morphology):
    for word in phrase.split(' '):
        if morph.parse(word)[0].tag.POS == morphology:
            return True
    return False



def check_phrase(phrase):
    if contains_morph(phrase, 'INFN') and (contains_morph(phrase, 'ADVB')):
        return True
    elif contains_morph(phrase, 'NOUN') and (contains_morph(phrase, 'ADJF')):
        return True
    else:
        return False

# if __name__ == '__main__':
#     driver = webdriver.Chrome('D:/chromedriver_win32/chromedriver.exe')
#     driver.get('https://www.google.com/maps/place/Mirador+Torre+Latino/@19.43393,-99.14056,17z/data=!4m7!3m6!1s0x85d1f92b5aafce31:0x61c3913b34ed5a63!8m2!3d19.4339303!4d-99.14056!9m1!1b1')
#     time.sleep(2)
#     try:
#         print(789)
#         element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cYrDcjyGO77__container'))
#         WebDriverWait(driver, 5).until(element_present)
#         print(456)
#     except Exception as e:
#         print(123)
#     review_menu = driver.find_element_by_css_selector(
#         'div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
#     )
#     print(review_menu)
#     time.sleep(4)
#     driver.refresh()

def convert(item):
    date_range = item
    range = ''.join(filter(str.isdigit, date_range))
    date_range = re.sub("\d+", "", date_range).replace("назад", "").strip()
    if range is '':
        range = 1
    range = int(range)
    if date_range in ('дней', "дня"):
        date_range = datetime.datetime.now() - relativedelta(days=range)
    elif date_range in ('недели, неделю'):
        date_range = datetime.datetime.now() - relativedelta(weeks=range)
    elif date_range in ('месяцев', "месяца", "месяц"):
        date_range = datetime.datetime.now() - relativedelta(months=range)
    elif date_range in ("год", "года", "лет"):
        date_range = datetime.datetime.now() - relativedelta(years=range)
    elif date_range == 'вчера':
        date_range = datetime.datetime.now() - relativedelta(days=1)
    elif date_range == 'часов':
        date_range = datetime.datetime.now()
    # print(range)
    date_range = datetime.datetime.strftime(date_range, '%Y-%m-%d')
    print(date_range)
    item = date_range
    return item


def clear_results():
    # file = pandas.read_csv('analyse_result/current_result/berlin_tf_idf_words.csv')
    results = []
    file_name = ''
    for file in glob.glob("loads/current_load/*_tf_idf_words.csv"):
        file_name = os.path.basename(file)
        with open(file, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                print(file_name)
                if row.__getitem__(1) == 'words':
                    results.append(row)
                    continue
                print(row)
                row[8] = convert(row[8])
                results.append(row)
        with open('analyse_result/current_result/' + file_name, 'w+', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(results)


# update_query("insert into parameters (name, value) values ('load_place', 'tokio_tower');")


if __name__ == '__main__':
    db_load.save_to_db()