from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .User import User
from .Item import Item

Base = declarative_base()


class Char(Base):
    __tablename__ = "chars"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    lvl = Column(Integer, nullable=False, default=1)
    rank = Column(Integer, nullable=False, default=1)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    balance = Column(Integer, default=0)
    class_name = Column(String, nullable=False)
    race = Column(String, nullable=False)
    strength = Column(Integer, default=1)
    agility = Column(Integer, default=1)
    smart = Column(Integer, default=1)

    head = Column(Integer, ForeignKey(Item.id))
    body = Column(Integer, ForeignKey(Item.id))
    legs = Column(Integer, ForeignKey(Item.id))
    boots = Column(Integer, ForeignKey(Item.id))

    weapon = Column(Integer, ForeignKey(Item.id))

    def __init__(self, name, lvl, rank, user_id, balance, class_name, race, strength, agility, smart):
        self.name = name
        self.lvl = lvl
        self.rank = rank
        self.user_id = user_id
        self.balance = balance
        self.class_name = class_name
        self.race = race
        self.strength = strength
        self.agility = agility
        self.smart = smart

    def __repr__(self):
        return f"User({self.name}, {self.lvl}, {self.rank}, {self.user_id})"



