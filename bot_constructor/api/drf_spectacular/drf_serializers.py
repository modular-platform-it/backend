# type: ignore
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Сериализатор для отображения ендпоинта в swagger"""

    email = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    """Сериализатор для отображения ендпоинта в swagger"""
