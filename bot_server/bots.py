import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from db import Connection
from handlers import router
from models import Bots


class TelegramBot:
    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.connection = Connection()
        self.bot_data = self.connection.session.query(Bots).filter(Bots.id == bot_id).first()
        self.token = self.bot_data.token
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher()
        # self.dispatcher.include_router(router1)
        self.commands = [
            BotCommand(command="/start", description=f"Start the bot {self.bot_data.name}"),
        ]

    async def start(self):
        print('Bot started')
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.start_polling(self.bot)


if __name__ == "__main__":
    bot = TelegramBot(bot_id=6)
    asyncio.run(bot.start())
