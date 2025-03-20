from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# Ассоциативная таблица для связи "многие ко многим" между услугами и врачами
service_doctor_association = Table(
    "service_doctor_association",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True),
    Column("doctor_id", Integer, ForeignKey("doctors.id"), primary_key=True)
)

# Ассоциативная таблица для связи "многие ко многим" между клиниками и услугами
clinic_service_association = Table(
    "clinic_service_association",
    Base.metadata,
    Column("clinic_id", Integer, ForeignKey("clinics.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True)
)


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    duration = Column(Integer, nullable=True)
    logo_url = Column(String, nullable=True)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))

    # Связь с клиникой (можно оставить, если клиника только одна на услугу)
    clinic = relationship("Clinic", back_populates="services")

    # Связь с врачами через ассоциативную таблицу
    doctors = relationship("Doctor", secondary=service_doctor_association, back_populates="services")
    appointments = relationship('Appointment', back_populates='service')
    # Связь с клиниками через ассоциативную таблицу
    clinics = relationship("Clinic", secondary=clinic_service_association, back_populates="services")
