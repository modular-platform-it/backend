import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from db import Connection
from models import Bots, Actions
from aiogram.types import BotCommand
from aiogram.types import Message
from aiogram.filters import Command
"""Основа бота"""

connection = Connection()


class ConfigurableBot:
    def __init__(self, bot_id: str, commands: list):
        self.token = connection.session.query(Bots).filter(Bots.id==bot_id).first().token
        self.commands = commands or []

        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher()

    async def start_polling(self):
        await self.dispatcher.start_polling()


if __name__ == '__main__':
    commands: list = []
    configurable_bot = ConfigurableBot(1, commands=commands)
    configurable_bot.start_polling()

