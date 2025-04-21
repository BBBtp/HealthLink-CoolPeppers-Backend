from sqlalchemy import String
from sqlalchemy import Table, Column, Integer, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

from sqlalchemy.orm import relationship

Base = declarative_base()

class FavoriteType(PyEnum):
    DOCTOR = "doctor"
    CLINIC = "clinic"

class UserFavorite(Base):
    __tablename__ = 'user_favorites'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    item_id = Column(Integer, primary_key=True)
    item_type = Column(String, primary_key=True)

    # Связь с пользователем (User)
    user = relationship("User", back_populates="favorites")

    # Связь с клиникой или врачом в зависимости от item_type
    # Для упрощения, можно добавить условие, чтобы фильтровать, к чему относится запись.
    clinic = relationship("Clinic", primaryjoin="and_(UserFavorite.item_type == 'clinic', UserFavorite.item_id == Clinic.id)", back_populates="favorites")
    doctor = relationship("Doctor", primaryjoin="and_(UserFavorite.item_type == 'doctor', UserFavorite.item_id == Doctor.id)", back_populates="favorites")