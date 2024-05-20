from db import Connection
from models import TelegramBot

"""Добавление первого бота-тестогого"""
connection = Connection()
data = {
    "name": "bot3",
    "telegram_token": "7183394983:AAEzdAGDlbIoN4U129juaaUa7TdTu0SFEuU",
    "description": "sadsad",
    "api_key": "sadsad",  # pragma: allowlist secret
    "api_url": "http://api.sadsad.ru/",
    "api_availability": True,
    "bot_state": "RUNNING",
}

bot = TelegramBot(**data)

connection.session.add(bot)
connection.session.commit()
