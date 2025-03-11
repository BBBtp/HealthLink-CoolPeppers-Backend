from pydantic import BaseModel, condecimal

from app.db.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    appointment_id: int
    amount: condecimal(max_digits=10, decimal_places=2)


class PaymentConfirm(BaseModel):
    payment_id: int
    status: PaymentStatus


class Payment(BaseModel):
    id: int
    appointment_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    payment_url: str
    status: PaymentStatus

    class Config:
        from_attributes = True
