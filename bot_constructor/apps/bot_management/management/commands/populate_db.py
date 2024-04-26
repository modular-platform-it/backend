from typing import Any

from django.core.management import BaseCommand
from factory_data.factories import TelegramBotActionFactory, TelegramBotFactory


class Command(BaseCommand):
    help = "Заполняет БД тестовыми телеграм ботами."

    def add_arguments(self, parser) -> None:
        """Добавляет к команде аргумент - количество требуемых ботов."""
        parser.add_argument(
            "-a",
            "--amount",
            default=10,
            type=int,
            help="Количество создаваемых телеграм ботов.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Создает нужное количество ботов, к каждому 5 дополнительных действий."""
        telegram_bots = TelegramBotFactory.create_batch(options.get("amount"))
        for bot in telegram_bots:
            TelegramBotActionFactory.reset_sequence()
            TelegramBotActionFactory.create_batch(5, telegram_bot=bot)
