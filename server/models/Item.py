from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item:
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    icon = Column(BLOB)

    def __init__(self, name, icon):
        self.name = name
        self.icon = icon

    def __repr__(self):
        return f"Item({self.name}, {self.icon})"



