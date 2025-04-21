from sqlalchemy import String
from sqlalchemy import Table, Column, Integer, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class FavoriteType(PyEnum):
    DOCTOR = "doctor"
    CLINIC = "clinic"

user_favorites = Table(
    'user_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('item_id', Integer, primary_key=True),
    Column('item_type', String, primary_key=True)
)