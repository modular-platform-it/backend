import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from db import Connection
from models import Bots, Actions
"""Основна бота"""
connection = Connection()

bot_api = connection.session.query(Bots).filter(Bots.id==1).first().token

async def main():
    bot = Bot(token=bot_api)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())