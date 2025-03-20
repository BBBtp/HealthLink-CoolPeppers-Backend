from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.service import service_doctor_association
from app.db.session import Base

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    specialization = Column(String)
    description = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    experience = Column(Integer, nullable=True)
    customer_count = Column(Integer, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    rating = Column(Float, default=0.0)

    # Связь с клиникой (один ко многим)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    clinic = relationship("Clinic", back_populates="doctors")

    # Связь с услугами через ассоциативную таблицу
    services = relationship("Service", secondary=service_doctor_association, back_populates="doctors")
    appointments = relationship('Appointment', back_populates='doctor')
    # Связь с доступными слотами для записи (один ко многим)
    appointment_slots = relationship('AppointmentSlot', back_populates='doctor')
