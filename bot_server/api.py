import asyncio

from fastapi import FastAPI
from pydantic import BaseModel

from bots import BaseTelegramBot
from db import Connection
from models import TelegramBot

"""Шина общения и управление ботом"""
app = FastAPI()
connection = Connection()


class Bot(BaseModel):
    name: str
    token: str
    start: bool


@app.get("/{bot_id}/start/")
def start_bot(bot_id):
    bot_data = connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.start())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
