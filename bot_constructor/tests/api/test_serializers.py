from datetime import datetime, timedelta
from typing import Any

from api.serializers import (
    TelegramBotActionSerializer,
    TelegramBotCreateSerializer,
    TelegramBotSerializer,
    TelegramBotShortSerializer,
    TelegramFileSerializer,
)
from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from django.test import TestCase
from factory_data.factories import (
    TelegramBotActionFactory,
    TelegramBotFactory,
    TelegramBotFileFactory,
)


class TestTelegramBotSerialzier(TestCase):
    """Набор тестов для сериализаторов телеграм бота."""

    def setUp(self) -> None:
        now: datetime = datetime.now()
        self.data: dict[str, str | bool | datetime] = {
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
        """Проверка сериализатора для детального отображения."""
        serializer: TelegramBotSerializer = TelegramBotSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_telegram_bot_short_serializer(self):
        """Проверка сериализатора для отображения в списке."""
        serializer: TelegramBotShortSerializer = TelegramBotShortSerializer(
            data=self.data
        )
        self.assertTrue(serializer.is_valid())

    def test_telegram_bot_create_serializer(self):
        """Проверка сериализатора при создании."""
        serializer: TelegramBotCreateSerializer = TelegramBotCreateSerializer(
            data=self.data
        )
        self.assertTrue(serializer.is_valid())


class TestTelegramBotActionSerialzier(TestCase):
    """Набор тестов для сериализаторов действий телеграм бота."""

    def setUp(self) -> None:
        telegram_bot: TelegramBot = TelegramBotFactory.create()
        self.data: dict[str, str | bool | list[TelegramBotFile] | int] = {
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
        """Проверка корректной работы сериализатора."""
        serializer: TelegramBotActionSerializer = TelegramBotActionSerializer(
            data=self.data
        )
        self.assertTrue(serializer.is_valid())
