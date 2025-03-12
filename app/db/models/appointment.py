from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db.session import Base

class AppointmentStatus(PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    date = Column(DateTime)
    time = Column(String)
    status = Column(String, default=AppointmentStatus.pending)  # Статус записи: pending, confirmed, canceled
    user_id = Column(Integer, ForeignKey('users.id'))

    # Связи с другими таблицами
    clinic = relationship('Clinic')
    doctor = relationship('Doctor')
    service = relationship('Service')
    users = relationship('User', back_populates='appointments')
