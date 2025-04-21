from sqlalchemy import String
from sqlalchemy import Table, Column, Integer, ForeignKey, Enum
from enum import Enum as PyEnum

from sqlalchemy.orm import relationship

from app.db.session import Base


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