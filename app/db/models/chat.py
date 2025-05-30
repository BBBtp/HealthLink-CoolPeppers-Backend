from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Один из участников
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)# Второй участник
    created_at = Column(DateTime, default=func.now())
    #TODO: Когда юзер посетил врача и там будет кнопка которая редиректит на запись
    messages = relationship("Message", back_populates="chat")
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    doctor = relationship("Doctor")
