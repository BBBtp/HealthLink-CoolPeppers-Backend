from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    specialization = Column(String)
    description = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))

    # Связь с клиникой
    clinics = relationship('Clinic', back_populates='doctors')
    services = relationship('Service', back_populates='doctors')