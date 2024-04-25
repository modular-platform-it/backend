# type:ignore
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from celery import Celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Celery("bot_server", broker="redis://localhost:6379/0")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
router = Router()


@router.message(Command("start"))
async def command_start(message: Message):
    await message.answer("Привет! Это твой новый бот!")


@router.message(Command("stop"))
async def command_stop(message: Message):
    await message.answer(f"Пока {message.from_user.full_name}! До новых встреч!")


@app.task(name="test")
def run_bot(token):
    """Функция запуска бота."""
    bot = Bot(token)
    dispatcher = Dispatcher()
    command_start(dispatcher)
    dispatcher.start_polling(bot)


async def start_bots():
    bot = Bot(token="6363859330:AAF7IJ25UqNp2ymDfYt3dbztp3b2DUfom0w")
    run_bot.delay(bot.token)
    logger.info(f"Бот запущен.")


async def main():
    await start_bots()
    bot = Bot("6363859330:AAF7IJ25UqNp2ymDfYt3dbztp3b2DUfom0w")
    dispatcher = Dispatcher()
    dispatcher.include_routers(router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
