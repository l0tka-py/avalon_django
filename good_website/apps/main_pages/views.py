import datetime
from random import random

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


class CurrentDateView(View):
   def get(self, request):
       html = f"{datetime.datetime.now()}"
       return HttpResponse(html)


class Random(View):
    def get(self, request):
        return HttpResponse(random())


class MainPage(View):
    def get(self, request):
        return HttpResponse('<h1>Hello, World</h1>')


class IndexView(View):
    def get(self, request):
        return render(request, 'main_pages/index.html')


class Login(View):
    def get(self, request):
        return render(request, 'login/index.html')

    def post(self, request):
        return JsonResponse(request.POST, json_dumps_params={'indent': 4})
