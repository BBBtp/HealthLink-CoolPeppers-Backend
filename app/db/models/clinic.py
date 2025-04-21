from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from app.db.models.service import clinic_service_association
from app.db.session import Base


class Clinic(Base):
    __tablename__ = 'clinics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    metro = Column(String,nullable=True)
    description = Column(Text, nullable=True)
    work_time = Column(Text, nullable=True)
    year_foundation = Column(Integer, nullable=True)
    customers_count = Column(Integer, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    logo_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    price = Column(Integer, nullable=True)

    # Связь с услугами
    services = relationship("Service", secondary=clinic_service_association, back_populates="clinics")
    appointments = relationship('Appointment', back_populates='clinic')
    # Связь с врачами (один ко многим)
    doctors = relationship("Doctor", back_populates="clinic")
    favorites = relationship("UserFavorite", back_populates="clinic")
