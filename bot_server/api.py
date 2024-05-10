import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from bots import TelegramBot
"""Шина общения и управление ботом"""
app = FastAPI()

class Bot(BaseModel):
    name: str
    token: str
    start: bool

@app.get("/{bot_id}/start/")
def start_bot(bot_id):
    bot = TelegramBot(bot_id=bot_id)
    asyncio.run(bot.start())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)