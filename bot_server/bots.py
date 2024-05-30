import asyncio

import handlers
from aiogram import Bot, Dispatcher
from db import Connection
from log import py_logger, error_logger
from models import TelegramBot, TelegramBotAction
import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BotCommand, Message
from fastapi import HTTPException
from models_api import ItemList

connection = Connection()


class BaseTelegramBot:
    """Основа телеграмм Бота"""

    @error_logger
    def __init__(self, bot_data):
        self.bot_data = bot_data
        self.token = self.bot_data["telegram_token"]
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher()
        self.commands = []
        self.router = Router()
        # self.actions = (
        #     connection.session.query(TelegramBotAction)
        #     .filter(TelegramBotAction.telegram_bot_id == bot_data.id)
        #     .all()
        # )
        #
        # for action in self.actions:
        #     handler = getattr(handlers, action.action_type)(bot_data=self.bot_data)
        #     router = handler.router
        #     self.commands.append(handler.command)
        #     self.dispatcher.include_router(router)

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer("Привет!")
        py_logger.info(f"Бот создан ")

    @error_logger
    async def start(self):
        # py_logger.info(f"Бот стартовал {self.bot_data.id}")
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.start_polling(self.bot)

    @error_logger
    async def stop(self):
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.stop_polling()
        # py_logger.info(f"Бот остановлен {self.bot_data.id}")


if __name__ == "__main__":

    bot_data = connection.session.query(TelegramBot).filter(TelegramBot.id == 1).first()
    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.start())