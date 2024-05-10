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


class ResponseErrorSerializer(serializers.Serializer):
    """Сериализатор для ответа с кодом ошибок."""

    detail = serializers.CharField(default="error text")


class Response400Serializer(serializers.Serializer):
    """Сериализатор для ответа с кодом ошибки 400."""

    field_name = serializers.ListField(
        child=serializers.CharField(default="Invalid ID")
    )


class Response401Serializer(ResponseErrorSerializer):
    """Сериализатор для ответа с кодом ошибки 401."""


class Response404Serializer(ResponseErrorSerializer):
    """Сериализатор для ответа с кодом ошибки 404."""
