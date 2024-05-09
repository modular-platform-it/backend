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

async def start_bot(dp):
    await event_loop.create_task(dp.start_polling())

def bot_init(event_loop, token):
    bot = Bot(token)
    dp = Dispatcher(bot=bot)

    @router.message(Command("start"))
    async def process_start_command(message: Message):
        await message.reply("Привет!\nНапиши мне что-нибудь!")

    event_loop.run_until_complete(start_bot(dp))


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    tokens = connection.session.query(Bots).filter(Bots.id == 1).first().token
    bot_init(event_loop, tokens)

    event_loop.run_forever()