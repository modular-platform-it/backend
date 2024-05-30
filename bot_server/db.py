import os

from dotenv import load_dotenv
from log import py_logger
from models import Base
from sqlalchemy import URL, create_engine, inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import sessionmaker

load_dotenv()


class Connection:
    """Управление/инициализация БД и модели"""

    def __init__(self):
        # self.url_object = URL.create(
        #     drivername="postgresql+psycopg2",
        #     username=os.getenv("POSTGRES_USER", "postgres"),
        #     password=os.getenv("POSTGRES_PASSWORD", "456852"),
        #     host=os.getenv("DB_HOST", "localhost"),
        #     database=os.getenv("POSTGRES_DB", "postgres"),
        #     port=int(os.getenv("DB_PORT", "5439")),
        # )
        self.url_object = "sqlite:///foo.db"
        self.engine = create_engine(
            self.url_object,
            echo=True,
            client_encoding="utf8",
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.inspector: Inspector | None = inspect(subject=self.engine)
        py_logger.info(f"к базе подключились")


class DB:
    """Создание в БД таблиц"""

    def __init__(self):
        self.connection = Connection()

    def to_db(
        self,
    ):
        Base.metadata.create_all(
            bind=self.connection.engine,
        )
        self.connection.session.commit()


def run():
    db = DB()
    db.to_db()


if __name__ == "__main__":
    """Если надо инициилизировать БД"""
    run()
