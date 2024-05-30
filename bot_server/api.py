# Шина общения и управление ботом
import asyncio
import os

import sentry_sdk
from bots import BaseTelegramBot
from db import Connection
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from log import py_logger, error_logger
from models import TelegramBot
from models_api import EditBot
from pydantic import BaseModel
import threading

# import concurrent.futures # для MacOS


load_dotenv()
sentry_sdk.init(
    dsn=os.getenv(
        "DNS_SENTRY",
        "https://23e6d5f2732c51c6e2fcae66eb80c996@o4507328929398784.ingest.de.sentry.io/4507328931364944",
    ),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
app = FastAPI()
connection = Connection()


class Bot(BaseModel):
    name: str
    token: str
    start: bool

@error_logger
@app.get("/check/")
def check_app():
    return "Все работает"

@error_logger
@app.get("/{bot_id}/start/")
def start_bot(bot_id):
    # bot_data = (
    #     connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    # )
    if bot_id == 1:
        bot_data = {
            "name": "bot3",
            "telegram_token": "5887317990:AAH9l1nK1J8UPolkr03luFxBt5xTNtdUU1A",
            "description": "sadsad",
            "api_key": "sadsad",  # pragma: allowlist secret
            "api_url": "http://api.sadsad.ru/",
            "api_availability": True,
            "bot_state": "RUNNING",
        }
    else:
        bot_data = {
            "name": "bot4",
            "telegram_token": "7183394983:AAEzdAGDlbIoN4U129juaaUa7TdTu0SFEuU",
            "description": "sadsad",
            "api_key": "sadsad",  # pragma: allowlist secret
            "api_url": "http://api.sadsad.ru/",
            "api_availability": True,
            "bot_state": "RUNNING",
        }
    bot = BaseTelegramBot(bot_data=bot_data)
    # with concurrent.futures.ThreadPoolExecutor() as executor: # для MacOS - добавить строки во всех api
    #     executor.submit(bot.start)
    asyncio.run(bot.start())  # для MacOS - убрать строку
    py_logger.info(f"Бот запущен {bot_id}")
    return "Бот запущен"

@error_logger
@app.get("/{bot_id}/stop/")
def stop_bot(bot_id):
    bot_data = (
        connection.session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    )
    if not bot_data:
        return HTTPException(status_code=404, detail="Бот не найден")
    bot = BaseTelegramBot(bot_data=bot_data)
    asyncio.run(bot.stop())
    py_logger.info(f"Бот запущен {bot_id}")
    return "Бот остановлен"



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
