from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Skill(Base):
    __tablename__ = "skils"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    price = Column(Integer, default=0)
    damage = Column(Integer, default=0)

    def __init__(self, name, price, damage):
        self.name = name
        self.price = price
        self.damage = damage

    def __repr__(self):
        return f"Skill({self.name}, {self.price}, {self.damage})"


