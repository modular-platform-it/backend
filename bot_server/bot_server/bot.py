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
from asgiref.sync import sync_to_async
from bot_constructor.apps.bot_management.models import TelegramBot
from celery import Celery

app = Celery("bot_server", broker="redis://localhost:6379/0")
app.config_from_object("django.conf:settings", namespace="CELERY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def command_start(message: Message):
    await message.answer(f"Привет {message.from_user.full_name}! Это твой новый бот!")


@router.message(Command("stop"))
async def command_stop(message: Message):
    await message.answer(f"Пока {message.from_user.full_name}! До новых встреч!")


@app.task(name="tasks.celery")
def run_bot(bot_id):
    """Функция запуска бота."""
    telegram_bot = TelegramBot.objects.get(pk=bot_id)
    bot_token = telegram_bot.telegram_token
    bot = Bot(token=bot_token)
    dispatcher = Dispatcher(bot)
    command_start(dispatcher)
    dispatcher.start_polling()


async def start_bots():
    bots = await sync_to_async(list)(TelegramBot.objects.filter(is_started=False))
    for bot in bots:
        run_bot.delay(bot.telegram_token)
        logger.info(f"Бот {bot.name} запущен.")


async def main():
    await start_bots()
    bot = await sync_to_async(list)(TelegramBot.objects.filter(is_started=False))
    if bot:
        dispatcher = Dispatcher()
        dispatcher.include_routers(router)
        await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
