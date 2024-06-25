import json
import random
import time

import requests
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from fastapi import HTTPException
from log import py_logger
from models import Base, TelegramBotAction
from models_api import Item, ItemList


async def get_list(api_key, api_url) -> ItemList:
    """Получить список из другого приложения по API и токену."""
    response = requests.get(
        url=api_url,
        headers={"Authorization": f"Token {api_key}"},

    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    items = [value["name"] for value in response.json()]
    return ItemList(items=items)


async def get_item(api_key: str = "", api_url: str = "http://localhost:8000/") -> Item:
    """Получить item из другого приложения по API и токену."""
    response = requests.get(
        url=api_url,
        headers={"Authorization": f"Token {api_key}"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return Item(item=response.json())


async def post_item(
    api_key: str = "", api_url: str = "http://localhost:8000/", data: dict = {}
) -> Item:
    """Post-запрос в стороннее приложения по API и токену."""
    json_data = json.loads(data["datas"])
    response = requests.post(
        url=api_url,
        headers={"Authorization": f"Token {api_key}"},
        json=json_data,
    )
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return Item(item=response.json())


def serialize_json_to_lines(data):
    serialized_data = json.dumps(data, indent=2)
    lines = serialized_data.split("\n")
    return "\n".join(lines)


def serialize_lines_to_json(data):
    serialized_data = json.dumps(data, indent=2)
    lines = serialized_data.split("\n")
    return "\n".join(lines)


class GetListHandler:
    """Хэндлер получения списка из стороннего приложения"""

    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = self.action.command_keyword
        self.description = self.action.description or self.command
        self.commands = [
            BotCommand(command=self.command, description=self.description),
        ]

        @self.router.message(Command(self.command[1:]))
        async def get_list_handler(msg: Message):
            item_list = await get_list(
                api_key=self.action.api_key, api_url=self.action.api_url
            )
            await msg.answer(f"Список из вашего приложения: {item_list.items}")


class StopHandler:
    """Хэндлер остановки бота"""

    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.message = self.action.message
        self.command = self.action.command_keyword
        self.commands = [
            BotCommand(
                command=self.command,
                description=f"stop the bot {self.bot_data.name}",
            ),
        ]

        @self.router.message(Command(self.command[1:]))
        async def stop_handler(msg: Message):
            await msg.answer(self.message)


class Handlers:
    """Хэндлер запуска бота"""

    def __init__(self, bot_data, action, connection):
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = self.action.command_keyword
        self.message = self.action.message
        self.commands = [
            BotCommand(
                command=self.action.command_keyword,
                description=f"start the bot {self.bot_data.name}",
            ),
        ]

        @self.router.message(Command(self.command[1:]))
        async def start_handler(msg: Message):
            await msg.answer(self.message)


class GetItem:
    def __init__(self, bot_data, action, connection):

        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = self.action.command_keyword
        self.description = self.action.description or self.command
        self.commands = [BotCommand(command=self.command, description=self.description)]
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="id", callback_data="search_id"),
                    InlineKeyboardButton(text="name", callback_data="search_name"),
                ],
            ]
        )

        class IDState(StatesGroup):
            id = State()
            name = State()

        @self.router.message(Command(self.command[1:]))
        async def start_get_method(msg: Message):
            await msg.reply("Каким способом искать", reply_markup=self.keyboard)

        @self.router.callback_query(F.data == "search_id")
        async def get_id_handler(callback: CallbackQuery, state: FSMContext):
            await state.set_state(IDState.id)
            await callback.message.answer("Введите код продукта")

        @self.router.callback_query(F.data == "search_name")
        async def get_id_handler(callback: CallbackQuery, state: FSMContext):
            await state.set_state(IDState.name)
            await callback.message.answer("Введите имя продукта")

        @self.router.message(IDState.id)
        async def get_item_handler(msg: Message, state: FSMContext):
            await state.update_data(id=int(msg.text))
            data = await state.get_data()
            item = await get_item(
                api_key=self.action.api_key,
                api_url=f"{self.action.api_url}{data['id']}/",
            )
            gen = serialize_json_to_lines(item.item)
            await state.clear()
            await msg.answer(f"Нужный вам объект: {gen}")

        @self.router.message(IDState.name)
        async def get_item_handler(msg: Message, state: FSMContext):
            await state.update_data(name=msg.text)
            data = await state.get_data()
            item = await get_item(
                api_key=self.action.api_key,
                api_url=f"{self.action.api_url}?name={data['name']}",
            )
            gen = serialize_json_to_lines(item.item)
            await state.clear()
            await msg.answer(f"Нужный вам объект: {gen}")


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
        self.words = []
        self.requirement_count_word = 5

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


class RandomListHandler:
    def __init__(self, bot_data, action, connection):
        """Список объектов и получение рандомного n Обьектов"""
        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.connection = connection
        self.commands = [
            BotCommand(command="/add_word", description=f"Добавить новое объект"),
            BotCommand(
                command="/get_words_list",
                description=f"Получить случайных объект",
            ),
            BotCommand(
                command="/change_length_list",
                description=f"Изменить количество выдаваемых слов",
            ),
        ]
        self.words = []
        self.requirement_count_word = 1

        class WordState(StatesGroup):
            item = State()
            length_list = State()

        @self.router.message(Command("change_length_list"))
        async def change_lengh(msg: Message, state: FSMContext):
            """Изменение длины списка объектов"""
            await state.set_state(WordState.length_list)
            await msg.answer(
                f"Сейчас количество = {self.requirement_count_word}\nВведите необходимое количество объектов для выдачи при команде get_words_list"
            )

        @self.router.message(WordState.length_list)
        async def get_change_lengh(msg: Message, state: FSMContext):
            await state.update_data(length_list=msg.text)
            self.requirement_count_word = int(msg.text)
            await state.clear()
            await msg.answer("Длина списка изменена")

        @self.router.message(Command("add_item"))
        async def start_add_item(msg: Message, state: FSMContext):
            """Добавление нового Объекта"""
            await state.set_state(WordState.item)
            await msg.answer("Введите, что добавить нужно")

        @self.router.message(WordState.item)
        async def get_new_item(msg: Message, state: FSMContext):
            await state.update_data(item=msg.text)
            data = await state.get_data()
            self.words.append(data)
            self.action.data = self.words
            await state.clear()
            await msg.answer("Объект добавлен")

        @self.router.message(Command("get_item_list"))
        async def get_word_list_handler(msg: Message):
            """Получение списка из n Объектов"""
            text = ""
            if self.requirement_count_word < len(self.words):
                for item in range(len(self.words)):
                    word = random.choice(self.words)
                    text += word + "\n"
            else:
                for item in self.words:
                    text += item + "\n"
            await msg.answer(f"Список ваших слов\n{text}")


class GetJoke:
    def __init__(self, bot_data, action, connection):

        self.bot_data = bot_data
        self.router = Router()
        self.action = action
        self.command = self.action.command_keyword
        self.description = self.action.description or self.command
        self.commands = [BotCommand(command=self.command, description=self.description)]
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Гиковские шутки", callback_data="chack"),
                    InlineKeyboardButton(text="От папы", callback_data="father"),
                    InlineKeyboardButton(text="сетап-панчлайн", callback_data="setup"),
                ],
            ]
        )

        @self.router.message(Command(self.command[1:]))
        async def start_get_method(msg: Message):
            await msg.reply("Какую шутка рассказать", reply_markup=self.keyboard)

        @self.router.callback_query(F.data == "chack")
        async def get_chack_joke(callback: CallbackQuery, state: FSMContext):
            item = await get_item(
                api_key="",
                api_url=f"https://geek-jokes.sameerkumar.website/api?format=json",
            )
            await callback.message.answer(item.item["joke"], reply_markup=self.keyboard)

        @self.router.callback_query(F.data == "setup")
        async def get_setup_joke(callback: CallbackQuery, state: FSMContext):
            item = await get_item(
                api_key="",
                api_url="https://official-joke-api.appspot.com/random_joke",
            )
            await callback.message.answer(item.item["setup"])
            time.sleep(1)
            await callback.message.answer(
                item.item["punchline"], reply_markup=self.keyboard
            )


class PostItem:
    def __init__(self, bot_data, action, connection):

        self.bot_data = bot_data
        self.router = Router()
        self.action = action

        self.command = self.action.command_keyword
        self.description = self.action.description or self.command
        self.commands = [BotCommand(command=self.command, description=self.description)]

        class PostState(StatesGroup):
            datas = State()

        @self.router.message(Command(self.command[1:]))
        async def start_post_item(msg: Message, state: FSMContext):
            await state.set_state(PostState.datas)
            await msg.answer(
                'Введите json, например:\n{"name":"asdasdas","telegram_token":"sadsadasdas"}'
            )

        @self.router.message(PostState.datas)
        async def post_data_item_(msg: Message, state: FSMContext):
            await state.update_data(datas=msg.text)
            data = await state.get_data()
            await state.clear()
            print(msg.text, self.action.api_key, self.action.api_url)
            item = await post_item(
                api_key=self.action.api_key, api_url=self.action.api_url, data=data
            )
            await msg.answer(f"Ответ:\n{item.item}")
