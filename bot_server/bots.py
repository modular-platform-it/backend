import asyncio

from aiogram import Bot, Dispatcher

from handlers import router
from db import Connection
from models import Bots
from aiogram.types import BotCommand

"""Основа бота"""

class TelegramBot:
    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.connection = Connection()
        self.token = self.connection.session.query(Bots).filter(Bots.id == bot_id).first().token
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(router)
        self.commands = [
            BotCommand(command="/start", description="Start the bot")
        ]

    async def start(self):
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.start_polling(self.bot)


if __name__ == "__main__":
    bot = TelegramBot(bot_id=1)
    asyncio.run(bot.start())