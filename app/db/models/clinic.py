from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class Clinic(Base):
    __tablename__ = 'clinics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)

    services = relationship("Service", back_populates="clinics")
    doctors = relationship("Doctor", back_populates="clinics")