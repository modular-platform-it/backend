import asyncio

import handlers
from aiogram import Bot, Dispatcher
from db import Connection
from log import py_logger
from models import TelegramBot, TelegramBotAction

connection = Connection()


class BaseTelegramBot:
    """Основа телеграмм Бота"""

    def __init__(self, bot_data):
        super().__init__()
        self.bot_data = bot_data
        self.token = self.bot_data.telegram_token
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher()
        self.commands = []
        with connection as session:
            self.actions = (
                session.query(TelegramBotAction)
                .filter(TelegramBotAction.telegram_bot_id == bot_data.id)
                .all()
            )

        for action in self.actions:
            handler = getattr(handlers, action.action_type)(bot_data=self.bot_data)
            router = handler.router
            self.commands.append(handler.command)
            self.dispatcher.include_router(router)
        py_logger.info(f"Бот создан {self.bot_data.id}")

    async def start(self):
        py_logger.info(f"Бот стартовал {self.bot_data.id}")
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.start_polling(self.bot)

    async def stop(self):
        await self.dispatcher.stop_polling()
        py_logger.info(f"Бот остановлен {self.bot_data.id}")


if __name__ == "__main__":

    with connection as session:
        bot_data = session.query(TelegramBot).filter(TelegramBot.id == 1).first()

    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.start())
