from typing import Any, List

from pydantic import BaseModel


class ItemList(BaseModel):
    items: List[str]


class Item(BaseModel):
    item: dict[str, Any]


class EditBot(BaseModel):
    name: str
    description: str
    telegram_token: str
    api_url: str
    api_key: str
    api_availability: bool
    bot_state: str
