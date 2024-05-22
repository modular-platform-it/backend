import handlers
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand


class BaseTelegramBot:
    """Основа телеграмм Бота"""

    def __init__(self, bot_data):
        super().__init__()
        self.bot_data = bot_data
        self.token = self.bot_data.telegram_token
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
            },
            {
                "name": "StopHandler",
            },
            {
                "name": "GetListHandler",
            },
        ]

        for action in actions:
            router = getattr(handlers, action["name"])(bot_data=self.bot_data).router
            self.dispatcher.include_router(router)

    async def start(self):
        print("Bot starting")
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.start_polling(self.bot)

    async def stop(self):
        print("Bot stopped")
        await self.bot.set_my_commands(commands=self.commands)
        await self.dispatcher.stop_polling(self.bot)


if __name__ == "__main__":
    import asyncio

    from db import Connection
    from models import TelegramBot

    connection = Connection()
    bot_data = connection.session.query(TelegramBot).filter(TelegramBot.id == 1).first()
    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.start())
