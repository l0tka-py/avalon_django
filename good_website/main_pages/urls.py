from django.urls import path

from .views import *

urlpatterns = [
   path('datetime/', CurrentDateView.as_view()),
   path('random/', Random.as_view()),
   path('', MainPage.as_view()),
   path('index_view/', IndexView.as_view()),
   path('login/', Login.as_view()),
]