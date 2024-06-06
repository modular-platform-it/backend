import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BotCommand, Message
from fastapi import HTTPException
from models_api import ItemList


async def get_list(api_key, api_url) -> ItemList:
    """Получить список из другого приложения по API и токену."""
    response = requests.get(
        api_url,
        headers={"Authorization": f"{api_key}"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    items = [value["name"] for value in response.json()]
    return ItemList(items=items)


class GetListHandler:
    """Хэндлер получения списка из стороннего приложения"""

    def __init__(self, bot_data):
        self.bot_data = bot_data
        self.router = Router()
        self.command = BotCommand(command="/get_list", description=f"get list")

        @self.router.message(Command("get_list"))
        async def get_list_handler(msg: Message):
            item_list = await get_list(
                api_key=self.bot_data.api_key, api_url=self.bot_data.api_url
            )
            await msg.answer(f"Список из вашего приложения: {item_list.items}")


class StopHandler:
    """Хэндлер остановки бота"""

    def __init__(self, bot_data):
        self.bot_data = bot_data
        self.router = Router()
        self.command = BotCommand(
            command="/stop", description=f"stop the bot {self.bot_data.name}"
        )

        @self.router.message(Command("stop"))
        async def stop_handler(msg: Message):
            await msg.answer("До новых встреч!")


class Handlers:
    """Хэндлер запуска бота"""

    def __init__(self, bot_data):
        self.bot_data = bot_data
        self.router = Router()
        self.command = BotCommand(
            command="/start", description=f"start the bot {self.bot_data.name}"
        )

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer("Привет!")


class SendMassage:
    def __init__(self):
        self.router = Router()