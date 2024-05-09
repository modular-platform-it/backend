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
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(router)

async def main():
    bot = ConfigurableBot(connection.session.query(Bots).filter(Bots.id==1).first().token)
    await bot.dispatcher.start_polling(bot.bot)

if __name__ == '__main__':
    asyncio.run(main())
