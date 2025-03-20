from xmlrpc.client import DateTime

from pydantic import BaseModel
from datetime import date, time, datetime

from app.db.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    clinic_id: int
    doctor_id: int
    service_id: int
class AppointmentCreate(AppointmentBase):
    status: str

class Appointment(AppointmentBase):
    id: int
    status: AppointmentStatus
    appointment_slot_id: int

    class Config:
        from_attributes = True
