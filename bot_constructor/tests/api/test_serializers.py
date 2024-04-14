from datetime import datetime, timedelta

from api.serializers import (
    TelegramBotActionSerializer,
    TelegramBotCreateSerializer,
    TelegramBotSerializer,
    TelegramBotShortSerializer,
)
from django.test import TestCase
from factory_data.factories import TelegramBotFactory


class TestTelegramBotSerialzier(TestCase):
    def setUp(self) -> None:
        now = datetime.now()
        self.data = {
            "name": "test",
            "telegram_token": "0000000001:" + 35 * "a",
            "api_key": "ierugh9843",
            "api_url": "http://127.0.0.1",
            "is_started": True,
            "bot_state": "DRAFT",
            "api_availability": True,
            "created_at": now - timedelta(hours=1),
            "started_at": now - timedelta(minutes=30),
        }
        return super().setUp()

    def test_telegram_bot_serializer(self):

        serializer = TelegramBotSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_telegram_bot_short_serializer(self):
        serializer = TelegramBotShortSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_telegram_bot_create_serializer(self):
        serializer = TelegramBotCreateSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())


class TestTelegramBotActionSerialzier(TestCase):
    def setUp(self) -> None:
        telegram_bot = TelegramBotFactory.create()
        self.data = {
            "telegram_bot": telegram_bot.id,
            "name": "test_action",
            "command_keyword": "/test",
            "message": "test",
            "files": [],
            "position": 2,
            "is_active": False,
        }
        return super().setUp()

    def test_telegram_bot_serializer(self):

        serializer = TelegramBotActionSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
