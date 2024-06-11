import json
import random

import requests
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BotCommand, Message
from fastapi import HTTPException
from log import py_logger
from models import Base, TelegramBotAction
from models_api import Item, ItemList


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
    lines = serialized_data.split("\n")
    return "\n".join(lines)


class GetListHandler:
    """Хэндлер получения списка из стороннего приложения"""

    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.commands = [
            BotCommand(command="/get_list", description=f"get list"),
        ]

        @self.router.message(Command("get_list"))
        async def get_list_handler(msg: Message):
            item_list = await get_list(
                api_key=self.bot_data.api_key, api_url=self.bot_data.api_url
            )
            await msg.answer(f"Список из вашего приложения: {item_list.items}")


class StopHandler:
    """Хэндлер остановки бота"""

    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.commands = [
            BotCommand(
                command="/stop", description=f"stop the bot {self.bot_data.name}"
            ),
        ]

        @self.router.message(Command("stop"))
        async def stop_handler(msg: Message):
            await msg.answer("До новых встреч!")


class Handlers:
    """Хэндлер запуска бота"""

    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.commands = [
            BotCommand(
                command="/start", description=f"start the bot {self.bot_data.name}"
            ),
        ]

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer("Привет!")


class SendMassage:
    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action


class GetItem:
    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.commands = [BotCommand(command="/get_item", description=f"get list")]

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
                api_key=self.bot_data.api_key,
                api_url=f"{self.action.api_url}/{data["id"]}",
            )
            gen = serialize_json_to_lines(item.item)
            await state.clear()
            await msg.answer(f"Нужный вам обьект: {gen}")


class RandomWordLearnListHandler:
    def __init__(self, bot_data, action, connection):
        """Словарик для запоминания слов"""
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.connection = connection
        self.commands = [
            BotCommand(command="/add_word", description=f"Добавить новое слово"),
            BotCommand(
                command="/get_words_list",
                description=f"Получить список ваших слов на сегодня",
            ),
        ]
        self.words = self.action.data or []
        self.requirement_count_word = 5
        with self.connection as session:
            self.action.data = {
                "words": "self.words",
            }
            session.commit()

        class WordState(StatesGroup):
            word = State()
            translate = State()

        @self.router.message(Command("add_word"))
        async def get_start_add_handler(msg: Message, state: FSMContext):
            """Добавление нового слова и его перевод в словарик"""
            await state.set_state(WordState.word)
            await msg.answer("Введите слово")

        @self.router.message(WordState.word)
        async def get_word_handler(msg: Message, state: FSMContext):
            await state.update_data(word=msg.text)
            await state.set_state(WordState.translate)
            await msg.answer("Введите его перевод")

        @self.router.message(WordState.translate)
        async def get_translate_handler(msg: Message, state: FSMContext):
            await state.update_data(translate=msg.text)
            await state.set_state(WordState.translate)
            data = await state.get_data()
            self.words.append(data)
            self.action.data = self.words
            await state.clear()
            await msg.answer("Слово добавлено")

        @self.router.message(Command("get_words_list"))
        async def get_word_list_handler(msg: Message):
            """Получение списка из 5 случайных слов"""
            text = ""
            if self.requirement_count_word < len(self.words):
                for item in range(len(self.words)):
                    word = random.choice(self.words)
                    text += word["word"] + " : " + word["translate"] + "\n"
            else:
                for item in self.words:
                    text += item["word"] + " : " + item["translate"] + "\n"
            await msg.answer(f"Список ваших слов\n{text}")
