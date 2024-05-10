from db import Connection
from models import Bots

"""Добавление первого бота-тестогого"""
connection = Connection()
data = {
    "name": 'bot3',
    "token": "7183394983:AAEzdAGDlbIoN4U129juaaUa7TdTu0SFEuU",
    "status": False
}
bot = Bots(**data)

connection.session.add(bot)
connection.session.commit()
