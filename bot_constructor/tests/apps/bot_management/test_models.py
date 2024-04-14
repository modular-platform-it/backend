from apps.bot_management.models import TelegramBotAction
from django.test import TestCase
from factory_data.factories import TelegramBotActionFactory, TelegramBotFactory


class TestTelegramBotModel(TestCase):
    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()

    def test_string_representation(self):
        self.assertEqual(self.telegram_bot.name, str(self.telegram_bot))

    def test_save_function(self):
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
    def setUp(self) -> None:
        self.telegram_bot = TelegramBotFactory.create()
        self.telegram_action = TelegramBotActionFactory(telegram_bot=self.telegram_bot)

    def test_string_representation(self):
        self.assertEqual(self.telegram_action.name, str(self.telegram_action))
