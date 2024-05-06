# type: ignore
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    pass


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()


class DummySerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return data

    def to_representation(self, instance):
        return instance

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DummyBotSerializer(DummySerializer):
    name = serializers.ListSerializer(child=serializers.CharField())
    description = serializers.ListSerializer(child=serializers.CharField())
    telegram_token = serializers.ListSerializer(child=serializers.CharField())
    api_key = serializers.ListSerializer(child=serializers.CharField())
    api_url = serializers.ListSerializer(child=serializers.CharField())


class DummyTokenSerializer(DummySerializer):
    detail = serializers.BooleanField()


class DummyTokenErrorSerializer(DummySerializer):
    token = serializers.ListSerializer(child=serializers.CharField())


class DummyActionSerializer(DummySerializer):
    name = serializers.ListSerializer(child=serializers.CharField())
    description = serializers.ListSerializer(child=serializers.CharField())
    command_keyword = serializers.ListSerializer(child=serializers.CharField())
    message = serializers.ListSerializer(child=serializers.CharField())
    api_key = serializers.ListSerializer(child=serializers.CharField())
    api_url = serializers.ListSerializer(child=serializers.CharField())
    position = serializers.ListSerializer(child=serializers.CharField())
    is_active = serializers.ListSerializer(child=serializers.CharField())


class DummyFileSerializer(DummySerializer):
    telegram_action = serializers.ListSerializer(child=serializers.CharField())
    file = serializers.ListSerializer(child=serializers.CharField())


class MethodNotAlowedSerializer(DummySerializer):
    detail = serializers.CharField()


class DummyStartStopBotSerializer(DummySerializer):
    detail = serializers.CharField()


class DummyNotAuthorized(DummySerializer):
    detail = serializers.CharField()
