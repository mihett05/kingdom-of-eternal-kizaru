from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .Char import Char
from .Item import Item


class RealItem(declarative_base()):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey(Item.id))
    char_id = Column(Integer, ForeignKey(Char.id))

    def __init__(self, item_id, char_id):
        self.item_id = item_id
        self.char_id = char_id

    def __repr__(self):
        return f"RealItem({self.item_id}, {self.char_id})"
