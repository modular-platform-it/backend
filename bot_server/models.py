from sqlalchemy import  PrimaryKeyConstraint, ForeignKeyConstraint, ForeignKey

from sqlalchemy import Column, Integer, String, ARRAY, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Bots(Base):
    __tablename__: str = 'bots'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), )
    token = Column(String(200),)
    actions = relationship("Actions")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='bots_pk'),
    )


class Actions(Base):
    __tablename__: str = 'actions'
    id = Column(Integer, primary_key=True)
    parameters = Column(ARRAY(JSON), nullable=True)
    bot_id = Column(Integer, ForeignKey('bots.id'))
    bot = relationship("Bots")

    __table_args__ = (
        ForeignKeyConstraint(
            ['bots_id'],
            ['bots.id']),
    )

