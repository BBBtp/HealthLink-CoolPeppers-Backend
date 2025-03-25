from pydantic import BaseModel
from datetime import datetime

class AppointmentSlotBase(BaseModel):
    doctor_id: int
    slot_time: datetime

class AppointmentSlotCreate(AppointmentSlotBase):
    pass

class AppointmentSlot(AppointmentSlotBase):
    id: int

    class Config:
        from_attributes = True

