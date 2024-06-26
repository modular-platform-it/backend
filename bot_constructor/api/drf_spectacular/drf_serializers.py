# type: ignore
from rest_framework import serializers


class NotFoundSerializer(serializers.Serializer):
    """Сериализатор для отображения схемы swagger при статусе 404."""

    detail = serializers.CharField()


class DummySerializer(serializers.Serializer):
    """
    Базовый сериализатор для отбражения схем swagger.
    Не использовать для сериализации данных.
    """

    def to_internal_value(self, data):
        return data

    def to_representation(self, instance):
        return instance

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DummyBotSerializer(DummySerializer):
    """Сериализатор для отображения схемы swagger для статуса 400 телеграм бота."""

    name = serializers.ListSerializer(child=serializers.CharField())
    description = serializers.ListSerializer(child=serializers.CharField())
    telegram_token = serializers.ListSerializer(child=serializers.CharField())
    api_key = serializers.ListSerializer(child=serializers.CharField())
    api_url = serializers.ListSerializer(child=serializers.CharField())


class DummyTokenSerializer(DummySerializer):
    """Сериализатор для отображения схемы swagger для статуса 200 токена бота."""

    detail = serializers.BooleanField()


class DummyTokenErrorSerializer(DummySerializer):
    """Сериализатор для отображения схемы swagger для статуса 400 токена бота."""

    token = serializers.ListSerializer(child=serializers.CharField())


class DummyActionSerializer(DummySerializer):
    """Сериализатор для схемы swagger для статуса 400 действия телеграм бота."""

    name = serializers.ListSerializer(child=serializers.CharField())
    description = serializers.ListSerializer(child=serializers.CharField())
    command_keyword = serializers.ListSerializer(child=serializers.CharField())
    message = serializers.ListSerializer(child=serializers.CharField())
    api_key = serializers.ListSerializer(child=serializers.CharField())
    api_url = serializers.ListSerializer(child=serializers.CharField())
    position = serializers.ListSerializer(child=serializers.CharField())
    is_active = serializers.ListSerializer(child=serializers.CharField())


class DummyFileSerializer(DummySerializer):
    """Сериализатор для схемы swagger для статуса 400 файла телеграм бота."""

    telegram_action = serializers.ListSerializer(child=serializers.CharField())
    file = serializers.ListSerializer(child=serializers.CharField())


class MethodNotAlowedSerializer(DummySerializer):
    """Сериализатор для схемы swagger для статуса 405."""

    detail = serializers.CharField()


class DummyStartStopBotSerializer(DummySerializer):
    """Сериализатор схемы swagger для статуса 400 для эндпоинта start_stop_bot."""

    detail = serializers.CharField()


class DummyNotAuthorized(DummySerializer):
    """Сериализатор для схемы swagger для статуса 401."""

    detail = serializers.CharField()


class DummyVariableSerializer(DummySerializer):
    """Сериализатор для схемы swagger для статуса 400 переменной телеграм бота."""

    name = serializers.ListSerializer(child=serializers.CharField())
    telegram_action = serializers.ListSerializer(child=serializers.CharField())
    variable_type = serializers.ListSerializer(child=serializers.CharField())


class DummyHeaderSerializer(DummySerializer):
    """Сериализатор swagger для статуса 400 заголовка http запроса телеграм бота."""

    name = serializers.ListSerializer(child=serializers.CharField())
    telegram_action = serializers.ListSerializer(child=serializers.CharField())


class ForbiddenSerializer(DummySerializer):
    detail = serializers.CharField()
