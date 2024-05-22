from datetime import datetime, timedelta
from typing import Any

from api.serializers import (
    TelegramBotCreateSerializer,
    TelegramBotSerializer,
    TelegramBotShortSerializer,
)
from apps.bot_management.models import TelegramBot, TelegramBotFile
from django.test import TestCase
from django.urls import reverse
from factory_data.factories import TelegramBotFactory  # type: ignore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestTelegramBotSerialzier(TestCase):
    """Набор тестов для сериализаторов телеграм бота."""

    def setUp(self) -> Any:

        now: datetime = datetime.now()
        self.data: dict[str, str | bool | datetime] = {
            "name": "test",
            "telegram_token": "0000000001:" + 35 * "a",
            "api_key": "ierugh9843",  # pragma: allowlist secret
            "api_url": "http://127.0.0.1",
            "is_started": True,
            "bot_state": "DRAFT",
            "api_availability": True,
            "created_at": now - timedelta(hours=1),
            "started_at": now - timedelta(minutes=30),
        }
        return super().setUp()

    def test_telegram_bot_serializer(self) -> None:
        """Проверка сериализатора для детального отображения."""
        serializer: TelegramBotSerializer = TelegramBotSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_telegram_bot_short_serializer(self) -> None:
        """Проверка сериализатора для отображения в списке."""
        serializer: TelegramBotShortSerializer = TelegramBotShortSerializer(
            data=self.data
        )
        self.assertTrue(serializer.is_valid())

    def test_telegram_bot_create_serializer(self) -> None:
        """Проверка сериализатора при создании."""
        serializer: TelegramBotCreateSerializer = TelegramBotCreateSerializer(
            data=self.data
        )
        self.assertTrue(serializer.is_valid())


class TestTelegramBotActionSerialzier(APITestCase):
    """Набор тестов для сериализаторов действий телеграм бота."""

    def setUp(self) -> Any:
        self.telegram_bot: TelegramBot = TelegramBotFactory.create()
        self.data: dict[str, str | bool | list[TelegramBotFile] | int] = {
            "telegram_bot": self.telegram_bot.id,
            "name": "test_action",
            "command_keyword": "/test",
            "message": "test",
            "files": [],
            "position": 2,
        }
        return super().setUp()

    def test_telegram_bot_serializer(self) -> None:
        """Проверка корректной работы сериализатора."""

        response: Response = self.client.post(
            reverse(
                "telegram_bot-actions-list",
                kwargs={"telegram_bot_pk": self.telegram_bot.id},
            ),
            data=self.data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
