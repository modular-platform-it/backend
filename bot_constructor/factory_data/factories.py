# type:ignore
import sys
from datetime import timedelta

from apps.bot_management.models import TelegramBot, TelegramBotAction, TelegramBotFile
from django.conf import settings
from django.test import override_settings
from django.utils import timezone
from factory import Faker, Sequence, SubFactory, django, fuzzy
from faker_file.providers.txt_file import TxtFileProvider
from faker_file.storages.filesystem import FileSystemStorage

TEST_DIR = "test_dir"
if sys.argv[1] == "test":
    with override_settings(MEDIA_ROOT=TEST_DIR + "/media"):
        FS_STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")
else:
    FS_STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")
Faker.add_provider(TxtFileProvider)

cyrillic_letters = "".join(map(chr, range(ord("А"), ord("я") + 1))) + "Ёё"


class TelegramBotFactory(django.DjangoModelFactory):
    """Фабрика генерации объектов телеграм бота."""

    class Meta:
        model = TelegramBot

    name = fuzzy.FuzzyText(prefix="тест_", length=15, chars=cyrillic_letters)
    telegram_token = Faker("bothify", text=10 * "#" + ":" + 35 * "?")
    created_at = Faker("date_time_between", start_date=timedelta(days=30))
    started_at = Faker(
        "date_time_this_month", after_now=False, tzinfo=timezone.get_current_timezone()
    )
    api_key = Faker("bothify", text="???##?###???")
    api_url = Faker("uri")
    api_availability = Faker("pybool", truth_probability=70)
    bot_state = fuzzy.FuzzyChoice(TelegramBot.BotState.values)


class TelegramBotActionFactory(django.DjangoModelFactory):
    """Фабрика генерации объектов действий телеграм бота."""

    class Meta:
        model = TelegramBotAction

    telegram_bot = SubFactory(TelegramBotFactory)
    name = fuzzy.FuzzyText(prefix="тест_", length=10, chars=cyrillic_letters)
    command_keyword = Faker("bothify", text="/#####")
    message = Faker("sentence")
    position = Sequence(lambda n: n + 2)
    is_active = Faker("pybool", truth_probability=70)


class TelegramBotFileFactory(django.DjangoModelFactory):
    """Фабрика генерации объектов файлов телеграм бота."""

    class Meta:
        model = TelegramBotFile

    telegram_action = SubFactory(TelegramBotActionFactory)
    file = Faker("txt_file", storage=FS_STORAGE)
