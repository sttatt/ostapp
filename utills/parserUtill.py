# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time, random, traceback, datetime, os
import json

# TODO Все перевести на параметры
# TODO Добавить метки времени
# TODO Добавить проверку уникальности
# TODO Добавить сбор по разным сортировкам
# TODO Добавить многопоточность
# TODO Убрать time.sleep

PARAMETERS = {}
PLACE_VALUE = ''
PLACE = 'place'
ID = 'id'
TEXT = 'text'
DATE = 'date'
STARS = 'stars'
REVIEW_QUANTITY = 'review_quantity'
STARS_SPAN = 'stars_span'
STARS_NUM_SPAN = 'stars_num_span'
DATE_SPAN = 'date_span'
DATE_SOURCE_SPAN = 'date_source_span'
FIELDNAMES = [ID, TEXT, REVIEW_QUANTITY, STARS, DATE, 'date_create', 'order_type']
CLASS_FINDERS = {
    # 'id' : 'data-review-id',
    TEXT: 'div.section-review-review-content',
    DATE: 'span.section-review-publish-date',
    STARS: 'div.section-review-metadata.section-review-metadata-with-note',
    REVIEW_QUANTITY: 'div.section-review-subtitle',
    STARS_SPAN : 'span.section-review-stars',
    STARS_NUM_SPAN : 'span.section-review-numerical-rating',
    DATE_SOURCE_SPAN : 'span.section-review-publish-date-and-source',
    DATE_SPAN : 'span.section-review-publish-date'
}

# sites = {
#     'burj_al_arab' :
#     'https://www.google.com/maps/place/%D0%91%D1%83%D1%80%D0%B4%D0%B6+%D0%90%D0%BB%D1%8C+%D0%90%D1%80%D0%B0%D0%B1/@25.1415548,55.183884,18z/data=!4m10!3m9!1s0x3e5f6a576414cf2d:0xb3da71b879f0e038!5m2!4m1!1i2!8m2!3d25.1411914!4d55.1852468!9m1!1b1'
#     ,
#     'eifel_tower' :
#     'https://www.google.com/maps/place/%D0%AD%D0%B9%D1%84%D0%B5%D0%BB%D0%B5%D0%B2%D0%B0+%D0%B1%D0%B0%D1%88%D0%BD%D1%8F/@48.8557273,2.293761,16z/data=!4m10!1m2!3m1!2z0K3QudGE0LXQu9C10LLQsCDQsdCw0YjQvdGP!3m6!1s0x47e66e2964e34e2d:0x8ddca9ee380ef7e0!8m2!3d48.8583702!4d2.2944823!9m1!1b1'
#     ,
#     'empire_state_building' :
#     'https://www.google.com/maps/place/%D0%AD%D0%BC%D0%BF%D0%B0%D0%B9%D1%80-%D1%81%D1%82%D0%B5%D0%B9%D1%82-%D0%B1%D0%B8%D0%BB%D0%B4%D0%B8%D0%BD%D0%B3/@40.7484405,-73.9856644,17z/data=!4m7!3m6!1s0x89c259a9b3117469:0xd134e199a405a163!8m2!3d40.7484405!4d-73.9856644!9m1!1b1'
#     ,
#     'berlin_tower' :
#     'https://www.google.com/maps/place/%D0%91%D0%B5%D1%80%D0%BB%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F+%D1%82%D0%B5%D0%BB%D0%B5%D0%B1%D0%B0%D1%88%D0%BD%D1%8F/@52.520815,13.4072304,17z/data=!4m7!3m6!1s0x47a84e1f9014ffeb:0xc8fafc484349e4a1!8m2!3d52.520815!4d13.409419!9m1!1b1'
#     ,
#     'canton_tower' :
#     'https://www.google.com/maps/place/Canton+Tower+Wharf/@23.1063494,113.3210693,17z/data=!4m10!1m2!2m1!1zQ2FudG9uIFRvd2VyLCBIYWl6aHUgRGlzdHJpY3QsINCT0YPQsNC90YfQttC-0YMsINCa0LjRgtCw0Lk!3m6!1s0x3402ff6e90c63f4b:0x66415ccedb7abd0a!8m2!3d23.107019!4d113.318771!9m1!1b1'
#     ,
#     'torre_latino_tower' :
#     'https://www.google.com/maps/place/Mirador+Torre+Latino/@19.43393,-99.14056,17z/data=!4m7!3m6!1s0x85d1f92b5aafce31:0x61c3913b34ed5a63!8m2!3d19.4339303!4d-99.14056!9m1!1b1'
#     ,
#     'tai_pei_tower' :
#     'https://www.google.com/maps/place/Taipei+101+Observatory/@25.0346396,121.562649,17z/data=!4m15!1m7!3m6!1s0x3442abb70399dad9:0x41fa82d6ef9a7db7!2zMTAxRGFsb3UybG91bGlhbnRvbmd0aWFuIEJyaWRnZSwgWGlueWkgRGlzdHJpY3QsIFRhaXBlaSBDaXR5LCDQotCw0LnQstCw0L3RjCAxMTA!3b1!8m2!3d25.0346396!4d121.5648377!3m6!1s0x3442abb6e9d93249:0xd508f7b3aa02d931!8m2!3d25.0336751!4d121.5648828!9m1!1b1'
#     ,
#     'tokio_tower' :
#     'https://www.google.com/maps/place/%D0%A2%D0%B5%D0%BB%D0%B5%D0%B2%D0%B8%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F+%D0%B1%D0%B0%D1%88%D0%BD%D1%8F+%D0%A2%D0%BE%D0%BA%D0%B8%D0%BE/@35.6586696,139.7432889,17z/data=!4m10!1m2!2m1!1stokio+tower!3m6!1s0x60188bbd9009ec09:0x481a93f0d2a409dd!8m2!3d35.6585805!4d139.7454329!9m1!1b1'
#     ,
#     'sidney_tower' :
#     'https://www.google.com/maps/place/Sydney+Tower+Eye/@-33.870451,151.2065713,17z/data=!4m7!3m6!1s0x6b12ae3fb870a0cb:0xe21b547d906c24ca!8m2!3d-33.870451!4d151.20876!9m1!1b1'
#     ,
#     'tallin_tower' :
#     'https://www.google.com/maps/place/%D0%A2%D0%B0%D0%BB%D0%BB%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F+%D1%82%D0%B5%D0%BB%D0%B5%D0%B1%D0%B0%D1%88%D0%BD%D1%8F/@59.4712094,24.8852614,17z/data=!4m7!3m6!1s0x4692ed17d6c120fd:0xfa7c6f2edafe1b19!8m2!3d59.4712094!4d24.8874501!9m1!1b1'
#     ,
#     'chicago_360' :
#     'https://www.google.com/maps/place/360+Chicago/@41.8989423,-87.6257324,17z/data=!4m7!3m6!1s0x880fd3541290b235:0x7314937a7703eb74!8m2!3d41.8989423!4d-87.6235437!9m1!1b1'
# }
#'ostankino_tower' : 'https://www.google.ru/maps/place/%D0%9E%D1%81%D1%82%D0%B0%D0%BD%D0%BA%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F+%D0%A2%D0%B5%D0%BB%D0%B5%D0%B1%D0%B0%D1%88%D0%BD%D1%8F/@55.8196818,37.6094739,17z/data=!4m7!3m6!1s0x46b5360d0c5eb911:0x6108436441c66f55!8m2!3d55.8196818!4d37.6116626!9m1!1b1'}



# Press the green button in the gutter to run the script.


# #def selenium_parse():
#     driver = webdriver.Chrome('D:/chromedriver_win32/chromedriver.exe')
#     #driver.get("https://yandex.ru/maps/10502/paris/?ll=2.294527%2C48.858255&mode=search&oid=21455091129&ol=biz&z=18.17")
#     #driver.get('https://yandex.ru/maps/213/moscow/?ll=37.611704%2C55.819721&mode=search&oid=1305642931&ol=biz&z=13.65')
#     driver.get('https://yandex.ru/maps/213/moscow/?ll=37.617887%2C55.751617&mode=poi&poi%5Bpoint%5D=37.618879%2C55.751426&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1023322799&z=16.16')
#     elem = driver.find_element_by_class_name('tabs-select-view__titles')
#     elems = elem.find_elements_by_class_name("carousel__item")
#     print(elems.__getitem__(1))
#     elem = elems.__getitem__(1)
#     print(elem.text)
#     elem.click()
#     try:
#         while True:
#             dialog = driver.find_element_by_class_name('dialog__content')
#             reviews = dialog.find_elements_by_class_name('business-review-view')
#             print(reviews.__len__())
#             # reviews = driver.find_elements_by_class_name('business-review-view')
#             more = dialog.find_element_by_class_name('reviews-view__more')
#             more.click()
#             time.sleep(random.randint(2, 4))
#     except Exception as e:
#         print('reviews is over')
#         print(traceback.format_exc())
#     dialog = dialog = driver.find_element_by_class_name('dialog__content')
#     reviews = dialog.find_elements_by_class_name('business-review-view')
#     print(reviews.__len__())
#     # elem = driver.find_element_by_class_name("card-feature-view__content")
#     # print(elem.text)
#     assert "No parse_results found." not in driver.page_source
#     driver.close()
#     print_hi('PyCharm')
def wait_loading(css_selector, timeout=5):
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        WebDriverWait(driver, timeout).until(element_present)
    except (TimeoutException, NoSuchElementException) as e:
        print(e.__class__.__name__+" class: "+css_selector)

def choose_order_test(link, count):
    driver = webdriver.Chrome('D:/chromedriver_win32/chromedriver.exe')
    driver.get(link)
    time.sleep(3)

    elem = driver.find_element_by_class_name('cYrDcjyGO77__container')
    elem.click()
    time.sleep(2)
    action = ActionChains(driver)
    action.move_to_element_with_offset(elem, 10, 30 + (30 * count))
    action.click()
    action.perform()
    time.sleep(3)

def load_review_menu(driver):
    try:
        print('trying to load review menu')
        wait_loading('div.section-layout.section-scrollbox.scrollable-y.scrollable-show', 15)
        review_menu = driver.find_element_by_css_selector(
            'div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
        )
        print('review menu loaded')
        return review_menu
    except NoSuchElementException as e:
        driver.refresh()
        print('review menu loading error')
        return load_review_menu(driver)


def choose_order(count, driver):
    try:
        wait_loading('div.cYrDcjyGO77__container', 15)
        elem = driver.find_element_by_class_name('cYrDcjyGO77__container')
        elem.click()
        action = ActionChains(driver)
        action.move_to_element_with_offset(elem, 10, 30+(30*count))
        time.sleep(3)
        action.click()
        time.sleep(3)
        action.perform()
    except (NoSuchElementException, TimeoutException) as e:
        driver.refresh()
        choose_order(count, driver)

def parse_google(link, count):
    global driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(PARAMETERS['webdriver_abs_path'], chrome_options=options)
    driver.get(link)
    try:
        choose_order(count, driver)
    except NoSuchElementException as e:
        print(e)
        if count > 0:
            return

    review_menu=load_review_menu(driver)

    driver.execute_script(
        'arguments[0].scrollTop = arguments[0].scrollHeight',
        review_menu
    )
    last_height = scroll(review_menu, driver)

    reviews = review_menu.find_elements_by_css_selector('div.section-review.ripple-container.GLOBAL__gm2-body-2')
    json_list = []
    print("Сбор отзывов...")
    for review in reviews:
        print('-------------------')
        review_id = review.get_attribute('data-review-id')
        print(review_id)
        classes = {}
        try:
            more_button = WebDriverWait(review, 0.5)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.section-expand-review.blue-link')))
            more_button.click()
            print('button clicked')
        except (NoSuchElementException, TimeoutException) as e:
            print('button not found')
        time.sleep(0.5)
        for class_name in FIELDNAMES:
            try:
                classes[class_name] = class_finder(class_name, review)
            except NoSuchElementException as e:
                print(class_name+' parsing error')
                print('review id: '+ review_id)
        classes[PLACE] = PLACE_VALUE
        classes['source'] = 'google_maps'
        try:
            classes['order_type'] = driver.find_element_by_css_selector('div.gm2-body-1.cYrDcjyGO77__label').text
        except NoSuchElementException as e:
            print('order type parsing error')
        json_list.append(classes)
        print(json_list.__len__())
    print('______________________________')
    print('Сбор отзывов закончен')
    print("Количество отзывов: "+str(json_list.__len__()))

    # path = PARAMETERS['results_directory']+PLACE_VALUE+'.json'
    # if not os.path.exists(path):
    #     open(path,'w').close()
    # with open(path,'r+',encoding='utf-8') as file:
    #     if os.stat(path).st_size != 0:
    #         data = json.load(file)
    #     else:
    #         data = []
    #     data = data+json_list
    #     file.seek(0)
    #     json.dump(data, file, indent=3, ensure_ascii=False)
    assert "No parse_results found." not in driver.page_source
    time.sleep(10)
    driver.close()
    return json_list

def scroll(elem, driver):
    print("Скроллинг страницы...")
    last_height = driver.execute_script("return arguments[0].scrollHeight", elem)
    try:
        while True:
            driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight',
                elem)
            time.sleep(5)
            new_height = driver.execute_script("return arguments[0].scrollHeight", elem)
            print('--------------------')
            print(last_height)
            print(new_height)
            if (int(PARAMETERS['test']) == 1):
                if last_height > 2000:
                    break
            else:
                if last_height == new_height:
                    break
            last_height = new_height
            print("Скроллинг закончен")
    except Exception as e:
        print('reviews is over')
        print(traceback.format_exc())

    return last_height



def class_finder(class_name, review):
    value = ''
    if class_name == ID:
        value = review.get_attribute('data-review-id')
    elif class_name == TEXT:
        value = review.find_element_by_css_selector(CLASS_FINDERS[TEXT]).text
    elif class_name == STARS:
        try:
            value = review.find_element_by_css_selector(CLASS_FINDERS[STARS_SPAN])\
                .get_attribute('aria-label')
            value = ''.join(filter(str.isdigit, value))
        except NoSuchElementException as e:
            print('stars not found. Trying to find numerical')
            value = review.find_element_by_css_selector(CLASS_FINDERS[STARS_NUM_SPAN]).text[0]
    elif class_name == DATE:
        try:
            value = review.find_element_by_css_selector(CLASS_FINDERS[DATE_SPAN]).text
        except NoSuchElementException as e:
            print('date not found. Trying to find date+source')
            value = review.find_element_by_css_selector(CLASS_FINDERS[DATE_SOURCE_SPAN])\
                .find_element_by_tag_name('span').text
    elif class_name == REVIEW_QUANTITY:
        try:
            value = review.find_element_by_css_selector(CLASS_FINDERS[REVIEW_QUANTITY])\
                .find_elements_by_tag_name('span').__getitem__(1).text
            value = ''.join(filter(str.isdigit, value))
        except NoSuchElementException as e:
            print('quantity not found')
    return value

def test():
    value = {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURRNUx2N2pBRRAB",
      "text": "Не в первый и дай Бог не в последний раз проинспектировал коммерческий символ Парижа.\nВывод -- Башня в хорошем состоянии!)\nНа первом этаже, около 60 метров, стального чуда Гюстава Эйфеля есть кафешка. Маленькая забегаловка для поклонников …",
      "review_quantity": "292",
      "stars": "4",
      "date": "3 года назад",
      "place": "eifel_tower"
   }
    value2 = {
      "id": "ChdDSUhNMG9nS0VJQ0FnSURRNUx2N2pBRRAB",
      "text": "Не в первый и дай Бог не в последний раз проинспектировал коммерческий символ Парижа.\nВывод -- Башня в хорошем состоянии!)\nНа первом этаже, около 60 метров, стального чуда Гюстава Эйфеля есть кафешка. Маленькая забегаловка для поклонников …",
      "review_quantity": "292",
      "stars": "4",
      "date": "3 года назад",
      "place": "eifel_tower"
   }
    values = {}
    values.append(value)
    values.append(value2)
    with open('../test.json', 'w', encoding='utf-8', ) as file:
        for val in values:
            json.dump(val, file, indent=3, ensure_ascii=False)

def clear_results():
    data = ''
    with open(PARAMETERS['results_directory']+PLACE_VALUE+'.json','r',encoding='utf-8') as r_file:
        data = json.load(r_file)
        for item in data:
            index = item['text'].find('Оригинал')
            if index != -1:
                item['text'] = item['text'][:index-3]
            translated = '(Переведено Google)'
            index = item['text'].find('(Переведено Google)')
            print(item['text'])
            if index != -1:
                item['text']= item['text'][index+translated.__len__()+1:]
                item['translated'] = True
            else:
                item['translated'] = False
            print(item['text'])
    #print(data)
    with open(PARAMETERS['no_trans_directory'] + PLACE_VALUE + '.json', 'w', encoding='utf-8') as w_file:
        #print(data)
        json.dump(data, w_file, ensure_ascii=False, indent=3)

def make_parse(name, link, params, count):
    global PLACE_VALUE
    global PARAMETERS
    PARAMETERS = params
    PLACE_VALUE = name
    return parse_google(link, count)


