from purchases.models import Cart, ShoppingCart
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров"""

    class Meta:
        model = Cart
        fields = ("id", "name", "measurement_unit", "description")


class ShoppingCartReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения товаров в список покупок"""

    cart = CartSerializer(required=True)

    class Meta:
        model = ShoppingCart
        fields = ("id", "user", "cart")


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи товаров в список покупок"""

    class Meta:
        model = ShoppingCart
        fields = ("id", "cart")
