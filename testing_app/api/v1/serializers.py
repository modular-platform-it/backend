
from rest_framework import serializers

from purchases.models import Cart, ShoppingCart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("id", "name", "measurement_unit", 'description')

class ShoppingCartReadSerializer(serializers.ModelSerializer):
    cart = CartSerializer(required=True)
    class Meta:
        model = ShoppingCart
        fields = ("id", "user", "cart")

class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ("id", "user", "cart")




