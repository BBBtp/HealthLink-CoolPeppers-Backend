from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.db.session import Base
from enum import Enum as PyEnum

class MessageStatus(PyEnum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User")
