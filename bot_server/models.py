# type:ignore
from datetime import datetime

from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_file import FileField

Base = declarative_base()


class TelegramBot(Base):
    __tablename__: str = "bot_management_telegrambot"
    id = Column(Integer, primary_key=True)
    name = Column(
        String(200),
    )
    telegram_token = Column(
        String(200),
    )
    description = Column(
        String(200),
    )
    api_key = Column(
        String(200),
    )
    api_url = Column(
        String(200),
    )
    api_availability = Column(
        Boolean,
    )
    bot_state = Column(
        String(200),
    )
    created_at = Column(DateTime, default=datetime.now)
    started_at = Column(DateTime)
    actions = relationship("TelegramBotAction")

    __table_args__ = (PrimaryKeyConstraint("id", name="bot_pk"),)


class TelegramBotAction(Base):
    __tablename__: str = "bot_management_telegrambotaction"
    id = Column(Integer, primary_key=True)
    telegram_bot_id = Column(Integer, ForeignKey("bot_management_telegrambot.id"))
    name = Column(
        String(200),
    )
    action_type = Column(
        String(200),
    )
    description = Column(
        String(200),
    )
    command_keyword = Column(
        String(200),
    )
    message = Column(
        String(200),
    )
    api_url = Column(
        String(200),
    )
    api_key = Column(
        String(200),
    )
    api_method = Column(
        String(200),
    )
    data = Column(
        JSON,
    )
    position = Column(
        Integer,
    )
    is_active = Column(
        Boolean,
    )
    next_action_id = Column(Integer, ForeignKey("bot_management_telegrambotaction.id"))

    __table_args__ = (
        PrimaryKeyConstraint("id", name="action_pk"),
        ForeignKeyConstraint(["telegram_bot_id"], ["bot_management_telegrambot.id"]),
        ForeignKeyConstraint(
            ["next_action_id"], ["bot_management_telegrambotaction.id"]
        ),
    )


class TelegramBotFile(Base):
    __tablename__: str = "bot_management_telegrambotfile"
    id = Column(Integer, primary_key=True)
    telegram_action_id = Column(
        Integer, ForeignKey("bot_management_telegrambotaction.id")
    )
    file = Column(
        FileField,
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", name="telegrambotfile_pk"),
        ForeignKeyConstraint(
            ["telegram_action_id"], ["bot_management_telegrambotaction.id"]
        ),
    )
