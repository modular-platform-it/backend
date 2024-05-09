from fastapi import FastAPI
from pydantic import BaseModel
from bots import TelegramBot
"""Шина общения и управление ботом"""
app = FastAPI()

class Bot(BaseModel):
    name: str
    token: str
    start: bool

@app.post("/{bot_id}/start/")
async def start_bot(bot_id):
    configurable_bot = TelegramBot(bot_id)
    # configurable_bot.start_polling()
    return {"message": "Hello World"}