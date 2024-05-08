from db import Connection
from models import Bots

"""Добавление первого бота-тестогого"""
connection = Connection()
data = {
    "name": 'bot',
    "token": "5887317990:AAH9l1nK1J8UPolkr03luFxBt5xTNtdUU1A",
    "status": False
}
bot = Bots(**data)

connection.session.add(bot)
connection.session.commit()
