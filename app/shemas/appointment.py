from xmlrpc.client import DateTime

from pydantic import BaseModel
from datetime import date, time, datetime


class AppointmentBase(BaseModel):
    clinic_id: int
    doctor_id: int
    service_id: int
    date_time: datetime
class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True
