from django.urls import path
from .views import CartView, WishlistView, ViewCartBuy, ViewCartAdd, ViewCartDel, CartViewSet, ViewWishAdd, ViewWishDel
from rest_framework import routers

app_name = 'cart_shop'

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)

urlpatterns = [
   path('', CartView.as_view(), name='cart'),
   path('wishlist', WishlistView.as_view(), name='wishlist'),
   path('buy/<int:product_id>', ViewCartBuy.as_view(), name='buy'),
   path('add/<int:product_id>', ViewCartAdd.as_view(), name='add_to_cart'),
   path('del/<int:item_id>', ViewCartDel.as_view(), name='del_from_cart'),
   path('add_wish/<int:product_id>', ViewWishAdd.as_view(), name='add_to_wish'),
   path('del_wish/<int:item_id>', ViewWishDel.as_view(), name='del_from_wish'),

]
