from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.session import Base


class PaymentStatus(PyEnum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    amount = Column(Float)
    payment_url = Column(String)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)  # Статус: pending, success, failed

    # Связь с записью
    appointment = relationship('Appointment')
