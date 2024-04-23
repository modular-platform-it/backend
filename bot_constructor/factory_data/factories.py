# type:ignore
from datetime import datetime, timedelta
from typing import IO

from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from django.conf import settings
from django.utils import timezone
from factory import Faker, Sequence, SubFactory, django, fuzzy
from faker_file.providers.txt_file import TxtFileProvider
from faker_file.storages.filesystem import FileSystemStorage

FS_STORAGE: str = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")
Faker.add_provider(TxtFileProvider)


class TelegramBotFactory(django.DjangoModelFactory):
    """Фабрика генерации объектов телеграм бота."""

    class Meta:
        model = TelegramBot

    name: str = Faker("company", locale="ru_RU")
    telegram_token: str = Faker("bothify", text=10 * "#" + ":" + 35 * "?")
    created_at: datetime = Faker("date_time_between", start_date=timedelta(days=30))
    started_at: datetime = Faker(
        "date_time_this_month", after_now=False, tzinfo=timezone.get_current_timezone()
    )
    api_key: str = Faker("bothify", text="???##?###???")
    api_url: str = Faker("uri")
    api_availability: bool = Faker("pybool", truth_probability=70)
    bot_state: tuple[str] = fuzzy.FuzzyChoice(TelegramBot.BotState.values)


class TelegramBotActionFactory(django.DjangoModelFactory):
    """Фабрика генерации объектов действий телеграм бота."""

    class Meta:
        model = TelegramBotAction

    telegram_bot: TelegramBot = SubFactory(TelegramBotFactory)
    name: str = Faker("company", locale="ru_RU")
    command_keyword: str = Faker("bothify", text="/#####")
    message: str = Faker("sentence")
    position: int = Sequence(lambda n: n + 2)
    is_active: bool = Faker("pybool", truth_probability=70)


class TelegramBotFileFactory(django.DjangoModelFactory):
    """Фабрика генерации объектов файлов телеграм бота."""

    class Meta:
        model = TelegramBotFile

    telegram_action: TelegramBotAction = SubFactory(TelegramBotActionFactory)
    file: IO = Faker("txt_file", storage=FS_STORAGE)
