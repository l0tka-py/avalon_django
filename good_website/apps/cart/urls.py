from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
   path('', view_cart, name='view_cart'),
   path('update_item/<int:item_id>/', update_item, name='update_item'),
   path('remove_item/<int:item_id>/', remove_item, name='remove_item'),
   path('checkout/', checkout, name='checkout'),
]
