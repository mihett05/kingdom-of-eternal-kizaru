from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .Char import Char
from .RealItem import RealItem
Base = declarative_base()


class Worn(Base):
    __tablename__ = "worn"
    id = Column(Integer, primary_key=True, autoincrement=True)
    realitem_id = Column(Integer, ForeignKey(RealItem.id))
    owner = Column(Integer, ForeignKey(Char.id))

    def __init__(self, realitem_id, owner_id):
        self.realitem_id = realitem_id
        self.owner = owner_id

    def __repr__(self):
        return f"Worn({self.realitem_id}, {self.owner})"



