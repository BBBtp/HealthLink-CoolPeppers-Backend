from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base
from enum import Enum as PyEnum

class UserRole(PyEnum):
    user = "user"
    doctor = "doctor"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=True, unique=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    photo_url = Column(String,nullable=True)
    age = Column(Integer, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    blood_type = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(String, default=UserRole.user.value,nullable=True)
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    appointments = relationship('Appointment', back_populates='user')
    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

