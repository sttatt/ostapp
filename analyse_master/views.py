from django.http import HttpResponse

from utills import db_utills
from services import algorithm1

def index(request):
    status = db_utills.select_one_item("SELECT status FROM analyse_sessions order by date_create desc limit 1")
    print(status)
    if status == 'work':
        return HttpResponse('Process in working')
    else:
        algorithm1.start()
    return HttpResponse("Analyse started")
