import requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import BotCommand, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from fastapi import HTTPException
from models_api import ItemList, Item
import json


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

async def get_item(api_key, api_url) -> Item:
    """Получить список из другого приложения по API и токену."""
    response = requests.get(
        api_url,
        headers={"Authorization": f"{api_key}"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return Item(item=response.json())


def serialize_json_to_lines(data):
    serialized_data = json.dumps(data, indent=2)
    lines = serialized_data.split('\n')
    return '\n'.join(lines)

class GetListHandler:
    """Хэндлер получения списка из стороннего приложения"""

    def __init__(self, bot_data, action):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = BotCommand(command="/get_list", description=f"get list")

        @self.router.message(Command("get_list"))
        async def get_list_handler(msg: Message):
            item_list = await get_list(
                api_key=self.bot_data.api_key, api_url=self.bot_data.api_url
            )
            await msg.answer(f"Список из вашего приложения: {item_list.items}")


class StopHandler:
    """Хэндлер остановки бота"""

    def __init__(self, bot_data, action):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = BotCommand(
            command="/stop", description=f"stop the bot {self.bot_data.name}"
        )

        @self.router.message(Command("stop"))
        async def stop_handler(msg: Message):
            await msg.answer("До новых встреч!")


class Handlers:
    """Хэндлер запуска бота"""

    def __init__(self, bot_data, action):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = BotCommand(
            command="/start", description=f"start the bot {self.bot_data.name}"
        )

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer("Привет!")


class SendMassage:
    def __init__(self, bot_data, action):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action


class GetItem:
    def __init__(self, bot_data, action):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = BotCommand(command="/get_item", description=f"get list")

        class IDState(StatesGroup):
            id = State()

        @self.router.message(Command("get_item"))
        async def get_id_handler(msg: Message, state: FSMContext):
            await state.set_state(IDState.id)
            await msg.answer("Введите код продукта")

        @self.router.message(IDState.id)
        async def get_item_handler(msg: Message, state: FSMContext):
            await state.update_data(id=int(msg.text))
            data = await state.get_data()
            item = await get_item(
                api_key=self.bot_data.api_key, api_url=f"{self.action.api_url}{data["id"]}"
            )
            gen = serialize_json_to_lines(item.item)
            await msg.answer(f"Нужный вам обьект: {gen}")
