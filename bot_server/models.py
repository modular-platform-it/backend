from sqlalchemy import (ARRAY, JSON, Boolean, Column, ForeignKey,
                        ForeignKeyConstraint, Integer, PrimaryKeyConstraint,
                        String)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Bots(Base):
    __tablename__: str = 'bots'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), )
    token = Column(String(200),)
    actions = relationship("Actions")
    status = Column(Boolean, default=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='bot_pk'),
    )


class Actions(Base):
    __tablename__: str = 'actions'
    id = Column(Integer, primary_key=True)
    parameters = Column(ARRAY(JSON), nullable=True)
    bot_id = Column(Integer, ForeignKey('bots.id'))

    __table_args__ = (
        ForeignKeyConstraint(
            ['bot_id'],
            ['bots.id']),
    )

