# Шина общения и управление ботом
import asyncio
import concurrent.futures  # для MacOS
import multiprocessing as mp
import os

import sentry_sdk
from bots import BaseTelegramBot
from db import Connection
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from log import error_logger, py_logger
from models import TelegramBot
from models_api import EditBot
from pydantic import BaseModel

load_dotenv()
sentry_sdk.init(
    dsn=os.getenv(
        "DNS_SENTRY",
        "https://23e6d5f2732c51c6e2fcae66eb80c996@o4507328929398784.ingest.de.sentry.io/4507328931364944",
    ),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
connection = Connection()


def run_fastapi(shared_data):
    import uvicorn

    app = FastAPI()
    # shared_data = shared_data

    @error_logger
    @app.get("/{bot_id}/start/")
    def start_bot(bot_id):
        shared_data.value = int(bot_id)
        print(shared_data.value)
        py_logger.info(f"Бот запущен {bot_id}")
        return "Бот запущен"

    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_aiogram(shared_data):
    import time

    while True:
        time.sleep(3)

        if shared_data.value != 0:
            bot_id = int(shared_data.value)
            bot_data = (
                connection.session.query(TelegramBot)
                .filter(TelegramBot.id == bot_id)
                .first()
            )

            bot = BaseTelegramBot(bot_data=bot_data)
            asyncio.run(bot.start())


if __name__ == "__main__":

    MAC = mp.Value("i", 0)
    MAC.value = 0
    # Создание процессов для FastAPI и Aiogram
    p1 = mp.Process(target=run_fastapi, args=(MAC,))
    p2 = mp.Process(target=run_aiogram, args=(MAC,))

    # Запуск процессов
    p1.start()
    p2.start()

    # Ожидание завершения процессов
    p1.join()
    p2.join()
