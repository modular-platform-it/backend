import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fastapi import HTTPException

from models import ItemList


class Handlers:
    """Логика работы ботов"""

    def __init__(self, bot_data):
        self.bot_data = bot_data
        self.router = Router()

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer("Привет!")

        async def get_list() -> ItemList:
            """Получить список из другого приложения по API."""
            response = requests.get(
                self.bot_data.api_url,
                headers={"Authorization": f"{self.bot_data.api_key}"},
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )
            items = [value["name"] for value in response.json()]
            return ItemList(items=items)

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
