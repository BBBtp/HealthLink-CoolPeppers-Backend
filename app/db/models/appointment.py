from sqlalchemy import Column, Integer, ForeignKey, String
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
    appointment_slot_id = Column(Integer, ForeignKey('appointment_slots.id'))  # Связь с таблицей слотов
    status = Column(String, default=AppointmentStatus.pending)  # Статус записи: pending, confirmed, canceled
    user_id = Column(Integer, ForeignKey('users.id'))

    # Связи с другими таблицами
    clinic = relationship('Clinic', back_populates='appointments')
    doctor = relationship('Doctor', back_populates='appointments')
    service = relationship('Service', back_populates='appointments')
    user = relationship('User', back_populates='appointments')
    appointment_slot = relationship('AppointmentSlot', back_populates='appointment')  # Связь с конкретным слотом записи
