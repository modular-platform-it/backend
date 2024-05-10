from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message


class Handlers:
    """Логика работы ботов"""

    def __init__(self):
        self.router = Router()

        @self.router.message(Command("start"))
        async def start_handler(msg: Message):
            await msg.answer(
                "Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение"
            )

        @self.router.message()
        async def message_handler(msg: Message):
            await msg.answer(f"Твой ID: {msg.from_user.id}")
