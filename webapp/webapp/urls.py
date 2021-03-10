"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('parse/', include('parse_master.urls')),
    path('analyse/', include('analyse_master.urls')),
    path('admin/', admin.site.urls),
]

from django.http import HttpResponse
from django.shortcuts import render
from services import Parser, Parse_loader
from utills import db_utills


# Create your views here.
# def index(request):
#     status = db_utills.select_one_item("SELECT status FROM parse_sessions order by date_create desc limit 1")
#     print(status)
#     if status == 'work':
#         return HttpResponse('Process in working')
#     else:
#         Parser.start()
#     return HttpResponse("Hello, world. You're at the polls index.")
#
# def load_results(request):
#     Parse_loader.load_results('all')
#     return HttpResponse("results loaded")
#
# def check_parse_status(request):
#     return ""