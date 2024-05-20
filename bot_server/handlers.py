import json

import requests
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from fastapi import HTTPException
from models import ItemList, TelegramBot

bot = TelegramBot()


async def get_list() -> ItemList:
    """Получить список из другого приложения по API."""
    # response = requests.get("https://api.xwick.ru/v1/bots/")
    response = requests.get(bot.api_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    items = [value["name"] for value in response.json()]
    return ItemList(items=items)


class Handlers:
    """Логика работы ботов"""

    def __init__(self):
        self.router = Router()

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer("Привет!")

        @self.router.message(Command("get_list"))
        async def get_list_handler(msg: Message):
            item_list = await get_list()
            await msg.answer(f"Список из вашего приложения: {item_list.items}")

        @self.router.message(Command("stop"))
        async def stop_handler(msg: Message):
            await msg.answer("До новых встреч!")


class SendMassage:
    def __init__(self):
        self.router = Router()
