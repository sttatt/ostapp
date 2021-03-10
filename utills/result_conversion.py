import json,re, datetime
from dateutil.relativedelta import relativedelta


def trans_results(item):
        index = item['text'].find('Оригинал')
        if index != -1:
            item['text'] = item['text'][:index-3]
        translated = '(Переведено Google)'
        index = item['text'].find('(Переведено Google)')
        if index != -1:
            item['text']= item['text'][index+translated.__len__()+1:]
            item['translated'] = True
        else:
            item['translated'] = False
        return item

def date_results(item):
    try:
        #{'месяцев', 'дней', 'недели', 'года', 'год', 'лет', 'вчера', 'месяца', 'месяц', 'дня', 'неделю'}
        date_range = item['date']
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
        #print(range)
        date_range = datetime.datetime.strftime(date_range, '%Y-%m-%d')
        item['converted_date'] = date_range
        item['date_create'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    except Exception as e:
        item['converted_date'] = None
        print('date_convertion_error. Item= '+item['id'])
    finally: return item

def convert_json(data):
    for item in data:
        item = trans_results(item)
        item = date_results(item)
    print("Конвертирование результата закончено")
    return data
