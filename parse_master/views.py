from django.http import HttpResponse

from utills import db_utills
from services import Parser, Parse_loader

def index(request):
    status = db_utills.select_one_item("SELECT status FROM parse_sessions order by date_create desc limit 1")
    print(status)
    if status == 'work':
        return HttpResponse('Process in working')
    else:
        Parser.start()
    return HttpResponse("Hello, world. You're at the polls index.")

def load_results(request):
    Parse_loader.load_results('all')
    return HttpResponse("results loaded")

def check_parse_status(request):
    return ""