# type:ignore
import asyncio

from bots import TelegramBot
from db import Connection
from fastapi import FastAPI
from models import Bots
from pydantic import BaseModel

"""Шина общения и управление ботом"""
app = FastAPI()
connection = Connection()


class Bot(BaseModel):
    name: str
    token: str
    start: bool


@app.get("/{bot_id}/start/")
def start_bot(bot_id):
    bot_data = connection.session.query(Bots).filter(Bots.id == bot_id).first()
    bot = TelegramBot(bot_data=bot_data)
    asyncio.run(bot.start())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
