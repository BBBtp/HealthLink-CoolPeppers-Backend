from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db.session import Base

class SlotStatus(PyEnum):
    available = "available"  # слот доступен
    booked = "booked"  # слот занят
    unavailable = "unavailable"  # слот недоступен

class AppointmentSlot(Base):
    __tablename__ = 'appointment_slots'

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    slot_time = Column(DateTime, nullable=False)  # Время приема
    status = Column(String, default=SlotStatus.available)  # Статус слота (доступен, занят, недоступен)

    # Связи с другими таблицами
    doctor = relationship('Doctor', back_populates='appointment_slots')
