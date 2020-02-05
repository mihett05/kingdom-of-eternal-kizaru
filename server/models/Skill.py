from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Skill(Base):
    __tablename__ = "skils"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    price = Column(Integer, default=0)
    damage = Column(Integer, default=0)
    class_name = Column(String)

    def __init__(self, name, price, damage, class_name):
        self.name = name
        self.price = price
        self.damage = damage
        self.class_name = class_name

    def __repr__(self):
        return f"Skill({self.name}, {self.price}, {self.damage})"


