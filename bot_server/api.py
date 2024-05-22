import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bots import BaseTelegramBot
from db import Connection
from models import TelegramBot
import concurrent.futures

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
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(bot.start)
    asyncio.run(bot.start())
    return "Бот запущен"


@app.get("/{bot_id}/stop/")
def stop_bot(bot_id):
    bot_data = (
        connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    )
    if not bot_data:
        return HTTPException(status_code=404, detail="Бот не найден")
    bot = BaseTelegramBot(bot_data=bot_data)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(bot.stop)
    asyncio.run(bot.stop())
    return "Бот остановлен"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
