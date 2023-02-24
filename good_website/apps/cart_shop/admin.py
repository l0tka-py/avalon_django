from django.contrib import admin
from .models import CartItemShop, Product, WishItemShop

admin.site.register(CartItemShop)
admin.site.register(WishItemShop)
admin.site.register(Product)

