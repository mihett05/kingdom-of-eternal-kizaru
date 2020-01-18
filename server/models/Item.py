from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    icon = Column(BLOB)
    price = Column(Integer, default=0)
    damage = Column(Integer, default=0)
    protect = Column(Integer, default=0)
    strength = Column(Integer, default=0)
    agility = Column(Integer, default=0)
    smart = Column(Integer, default=0)

    def __init__(self, name, icon=None, price=0, damage=0, protect=0, strength=0, agility=0, smart=0):
        self.name = name
        if icon is None:
            icon = ""  # Тут должна быть картинка
        self.icon = icon
        self.price = price
        self.damage = damage
        self.protect = protect
        self.strength = strength
        self.agility = agility
        self.smart = smart

    def __repr__(self):
        return f"Item({self.name}, None, {self.price}, {self.damage}, {self.protect}, {self.strength}," \
               f" {self.agility}, {self.smart})"



