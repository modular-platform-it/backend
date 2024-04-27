from apps.bot_management.models import TelegramBotAction
from django.test import TestCase
from factory_data.factories import (
    TelegramBotActionFactory,
    TelegramBotFactory,
    TelegramBotFileFactory,
)


class TestTelegramBotModel(TestCase):
    """Набор тестов модели телеграм бота."""

    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()

    def test_string_representation(self) -> None:
        """Проверка строкового представления модели телеграм бота."""
        self.assertEqual(self.telegram_bot.name, str(self.telegram_bot))

    def test_save_function(self) -> None:
        """Проверка создания действия бота при создании объекта телеграм бота."""
        self.assertTrue(
            TelegramBotAction.objects.filter(telegram_bot=self.telegram_bot).exists()
        )
        telegram_action, created = TelegramBotAction.objects.get_or_create(
            telegram_bot=self.telegram_bot.id, pk=1
        )
        self.assertFalse(created)
        self.assertEqual(telegram_action.name, "Старт")
        self.assertEqual(telegram_action.command_keyword, "/start")
        self.assertEqual(telegram_action.position, 1)
        self.assertEqual(telegram_action.is_active, True)


class TestTelegramBotActionModel(TestCase):
    """Набор тестов для модели действия телеграм бота."""

    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()
        self.telegram_action = TelegramBotActionFactory(telegram_bot=self.telegram_bot)

    def test_string_representation(self) -> None:
        """Проверка строкового представления модели действия телеграм бота."""
        self.assertEqual(self.telegram_action.name, str(self.telegram_action))


class TestTelegramBotActionFileModel(TestCase):
    """Набор тестов для модели файла действия телеграм бота."""

    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()
        self.telegram_action = TelegramBotActionFactory.create(
            telegram_bot=self.telegram_bot
        )
        self.telegram_file = TelegramBotFileFactory.create(
            telegram_action__telegram_bot=self.telegram_bot,
            telegram_action=self.telegram_action,
        )

    def test_string_representation(self) -> None:
        """Проверка строкового представления модели файла действия телеграм бота."""
        self.assertEqual(self.telegram_file.file.name, str(self.telegram_file))
