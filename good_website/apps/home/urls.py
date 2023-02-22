from django.urls import path

from .views import IndexShopView, AboutShopView, ContactShopView

app_name = 'home'

urlpatterns = [
   path('', IndexShopView.as_view(), name='index'),
   path('', AboutShopView.as_view(), name='about'),
   path('', ContactShopView.as_view(), name='contact'),

]
