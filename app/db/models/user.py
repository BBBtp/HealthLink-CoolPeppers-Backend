from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Хэш пароля
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    appointments = relationship('Appointment', back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

