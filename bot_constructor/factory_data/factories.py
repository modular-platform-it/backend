# type:ignore
from datetime import timedelta

from apps.bot_management.models import TelegramBot, TelegramBotAction
from django.utils import timezone
from factory import Faker, Sequence, SubFactory, django, fuzzy


class TelegramBotFactory(django.DjangoModelFactory):
    class Meta:
        model = TelegramBot

    name = Faker("company", locale="ru_RU")
    telegram_token = Faker("bothify", text=10 * "#" + ":" + 35 * "?")
    is_started = Faker("pybool", truth_probability=70)
    created_at = Faker("date_time_between", start_date=timedelta(days=30))
    started_at = Faker(
        "date_time_this_month", after_now=False, tzinfo=timezone.get_current_timezone()
    )
    api_key = Faker("bothify", text="???##?###???")
    api_url = Faker("uri")
    api_availability = Faker("pybool", truth_probability=70)
    bot_state = fuzzy.FuzzyChoice(TelegramBot.BotState.values)


class TelegramBotActionFactory(django.DjangoModelFactory):
    class Meta:
        model = TelegramBotAction

    telegram_bot = SubFactory(TelegramBotFactory)
    name = Faker("company", locale="ru_RU")
    command_keyword = Faker("bothify", text="/#####")
    message = Faker("sentence")
    position = Sequence(lambda n: n + 2)
    is_active = Faker("pybool", truth_probability=70)


## TODO
# class TelegramBotFileFactory(django.DjangoModelFactory):
#     class Meta:
#         model = TelegramBotFile

#     telegram_action = SubFactory(TelegramBotActionFactory)
#     file = SimpleUploadedFile("test.txt", content=b"Test")
