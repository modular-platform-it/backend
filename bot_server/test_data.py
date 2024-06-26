from db import Connection
from models import TelegramBot, TelegramBotAction

"""Добавление первого бота-тестогого"""
connection = Connection()
data1 = {
    "name": "bot3",
    "telegram_token": "5887317990:AAH9l1nK1J8UPolkr03luFxBt5xTNtdUU1A",
    "description": "sadsad",
    "api_key": "sadsad",  # pragma: allowlist secret
    "api_url": "http://api.sadsad.ru/",
    "api_availability": True,
    "bot_state": "RUNNING",
}
data2 = {
    "name": "bot4",
    "telegram_token": "7183394983:AAEzdAGDlbIoN4U129juaaUa7TdTu0SFEuU",
    "description": "sadsad",
    "api_key": "sadsad",  # pragma: allowlist secret
    "api_url": "http://api.sadsad.ru/",
    "api_availability": True,
    "bot_state": "RUNNING",
}

data_action1 = {
    "telegram_bot_id": 1,
    "name": "Получить итем",
    "command_keyword": "/get_item",
    "action_type": "GetItem",
    "description": "dsadasd",
    "api_url": "https://api.zippopotam.us/us/",
    "api_key": "",
    "data": {"name": 1},
}
data_action2 = {
    "telegram_bot_id": 1,
    "name": "Словарь",
    "command_keyword": "get_list",
    "action_type": "RandomWordLearnListHandler",
    "description": "dsadasd",
    "api_url": "https://api.zippopotam.us/us/",
    "api_key": "",
    "data": {"name": 1},
}
bot1 = TelegramBot(**data1)
# bot2 = TelegramBot(**data2)
action1 = TelegramBotAction(**data_action1)
action2 = TelegramBotAction(**data_action2)
with connection as session:
    # session.add(bot1)
    # session.add(bot2)
    # session.commit()
    session.add(action1)
    session.add(action2)
    session.commit()
