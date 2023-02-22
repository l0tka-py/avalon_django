from django.urls import path
from .views import CartView, WishlistView, ViewCartBuy, ViewCartAdd, ViewCartDel, CartViewSet
from rest_framework import routers

app_name = 'cart_shop'

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)

urlpatterns = [
   path('', CartView.as_view(), name='cart'),
   path('', WishlistView.as_view(), name='whishlist'),
   path('buy/<int:product_id>', ViewCartBuy.as_view(), name='buy'),
   path('add/<int:product_id>', ViewCartAdd.as_view(), name='add_to_cart'),
   path('del/<int:item_id>', ViewCartDel.as_view(), name='del_from_cart'),
]
