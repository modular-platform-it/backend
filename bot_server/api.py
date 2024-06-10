# Шина общения и управление ботом
import asyncio
import os
from contextlib import asynccontextmanager

import sentry_sdk
from bots import BaseTelegramBot
from db import Connection
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response
from log import py_logger
from models import TelegramBot
from models_api import EditBot
from pydantic import BaseModel

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


active_bots = dict()


@asynccontextmanager
async def start_bots(application: FastAPI):
    active_bots.clear()
    with connection as session:
        bots = session.query(TelegramBot).filter(TelegramBot.bot_state == "RUNNING")
    for bot_data in bots:
        bot = BaseTelegramBot(bot_data=bot_data)

        asyncio.get_event_loop().create_task(bot.start(), name=f"start_{bot_data.id}")

        active_bots[bot_data.id] = bot
        py_logger.info(f"Бот запущен {bot_data.id}")

    yield

    for bot in active_bots:
        asyncio.get_event_loop().create_task(bot.stop(), name=f"stop_{bot.bot_data.id}")
    active_bots.clear()


app = FastAPI(lifespan=start_bots)
connection = Connection()


class Bot(BaseModel):
    name: str
    token: str
    start: bool


@app.get("/check/")
async def check_app():
    # print("_________all_tasks_________")
    # for t in asyncio.all_tasks():
    #     print(t, "\n")
    # print("_____________")
    return Response("All ok")


@app.get("/{bot_id}/start/")
async def start_bot(bot_id: int):

    if active_bots.get(bot_id, None):
        tasks = asyncio.all_tasks()

        for task in tasks:
            if task.get_name() == f"start_{bot_id}":
                return Response("Already started.")

        active_bots.pop(bot_id)

    with connection as session:
        bot_data = session.query(TelegramBot).filter(TelegramBot.id == bot_id).first()
    if bot_data:
        bot = BaseTelegramBot(bot_data=bot_data)

        asyncio.get_event_loop().create_task(bot.start(), name=f"start_{bot_id}")

        active_bots[bot_id] = bot
        py_logger.info(f"Бот запущен {bot_id}")
        return Response("Bot started")
    else:
        py_logger.info(f"Бота нет {bot_id}")
        return Response("бот {bot_id} не существует")


@app.get("/{bot_id}/stop/")
async def stop_bot(bot_id: int):
    bot = active_bots.pop(bot_id, None)
    tasks = asyncio.all_tasks()
    for task in tasks:
        if task.get_name() == f"start_{bot_id}":
            break
    else:
        return HTTPException(status_code=404, detail="Bot not started")

    asyncio.get_event_loop().create_task(bot.stop(), name=f"stop_{bot_id}")

    py_logger.info(f"Бот запущен {bot_id}")
    return "Bot stopped"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
