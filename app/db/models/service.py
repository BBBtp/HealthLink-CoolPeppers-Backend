from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    duration = Column(Integer)
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))

    clinics = relationship('Clinic', back_populates='services')
    doctors = relationship('Doctor', back_populates='services')
