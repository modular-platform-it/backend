from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import sessionmaker

from models import Base


class Connection:
    """Управление/инициализация БД и модели"""

    def __init__(self):
        self.engine = create_engine(
            "postgresql+psycopg2://postgres:456852@localhost:5439/postgres?client_encoding=utf8",
            echo=True,
            client_encoding="utf8",
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.inspector: Inspector | None = inspect(subject=self.engine)


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
