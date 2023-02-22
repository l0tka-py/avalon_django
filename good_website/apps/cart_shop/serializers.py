from rest_framework import serializers
from .models import CartItemShop


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemShop
        fields = '__all__'
