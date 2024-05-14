import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from db import Connection
import handlers
from models import Bots


class TelegramBot:
    """Основа телеграмм Бота"""

    def __init__(self, bot_data: Bots):
        super().__init__()
        self.bot_data = bot_data
        self.token = self.bot_data.token
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher()
        self.commands = [
            BotCommand(
                command="/start", description=f"Start the bot {self.bot_data.name}"
            ),
        ]
        actions = [
            {
                "name": "Handlers",
                "parameters": {
                    "commands": None,
                }
            },
            {
                "name": "SendMassage",
                "parameters": {
                    "commands": None
                }
            },
        ]
        for action in actions:
            router = getattr(handlers, action["name"])().router
            self.dispatcher.include_router(router)

    async def start(self):
        print("Bot starting")
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.start_polling(self.bot)


if __name__ == "__main__":
    connection = Connection()
    bot_data = connection.session.query(Bots).filter(Bots.id == 1).first()
    bot = TelegramBot(bot_data=bot_data)
    asyncio.run(bot.start())
