from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .User import User

Base = declarative_base()


class Char(Base):
    __tablename__ = "chars"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    lvl = Column(Integer, nullable=False, default=1)
    rank = Column(Integer, nullable=False, default=1)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    balance = Column(Integer, default=0)

    def __init__(self, name, lvl, rank, user_id):
        self.name = name
        self.lvl = lvl
        self.rank = rank
        self.user_id = user_id

    def __repr__(self):
        return f"User({self.name}, {self.lvl}, {self.rank}, {self.user_id})"



