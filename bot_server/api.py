import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bots import BaseTelegramBot
from db import Connection
from models import TelegramBot, EditBot

# import concurrent.futures # для MacOS

"""Шина общения и управление ботом"""
app = FastAPI()
connection = Connection()


class Bot(BaseModel):
    name: str
    token: str
    start: bool


@app.get("/{bot_id}/start/")
def start_bot(bot_id):
    bot_data = (
        connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    )
    bot = BaseTelegramBot(bot_data=bot_data)
    # with concurrent.futures.ThreadPoolExecutor() as executor: для MacOS - добавить строки во всех api
    #     executor.submit(bot.start)
    asyncio.run(bot.start())  # для MacOS - убрать строку
    return "Бот запущен"


@app.get("/{bot_id}/stop/")
def stop_bot(bot_id):
    bot_data = (
        connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    )
    if not bot_data:
        return HTTPException(status_code=404, detail="Бот не найден")
    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.stop())
    return "Бот остановлен"


@app.put("/{bot_id}/edit/")
def edit_bot(bot_id, data: EditBot):
    bot_data = (
        connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    )
    if not bot_data:
        return HTTPException(status_code=404, detail="Бот не найден")
    bot_data.name = data.name
    bot_data.description = data.description
    bot_data.telegram_token = data.telegram_token
    bot_data.api_url = data.api_url
    bot_data.api_key = data.api_key
    bot_data.api_availability = data.api_availability
    bot_data.bot_state = data.bot_state
    connection.session.commit()
    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.edit())
    return "Бот изменен"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
