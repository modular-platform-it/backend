from db import Connection
from models import TelegramBot

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

bot1 = TelegramBot(**data1)
bot2 = TelegramBot(**data2)
with connection as session:
    session.add(bot1)
    session.add(bot2)
    session.commit()
