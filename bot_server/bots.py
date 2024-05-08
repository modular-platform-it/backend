import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from db import Connection
from models import Bots, Actions
from aiogram.types import BotCommand
"""Основа бота"""

connection = Connection()


class ConfigurableBot:
    def __init__(self, bot_id: str, commands: list):
        self.token = connection.session.query(Bots).filter(Bots.id==bot_id).first().token
        self.commands = commands or []

        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(storage=MemoryStorage())

    async def start_polling(self):
        for command in self.commands:
            BotCommand(command['command'], command['description'])

        await self.bot.set_my_commands(self.commands)
        await self.dp.start_polling()

    def add_command(self, command, description):
        self.commands.append({'command': command, 'description': description})


if __name__ == '__main__':
    configurable_bot = ConfigurableBot(1)

    configurable_bot.add_command('start', 'Start the bot')
    configurable_bot.add_command('help', 'Show help message')

    configurable_bot.start_polling()
