from pydantic import BaseModel
from datetime import date, time

class AppointmentBase(BaseModel):
    clinic_id: int
    doctor_id: int
    service_id: int
    date: date
    time: time

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True
