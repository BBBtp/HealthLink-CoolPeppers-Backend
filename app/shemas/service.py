from pydantic import BaseModel
from typing_extensions import Optional


class ServiceBase(BaseModel):
    name: str
    description: str
    price: float
    duration: int  # Длительность услуги в минутах

class ServiceCreate(ServiceBase):
    clinic_id: int
    doctor_id: int | None = None

class Service(ServiceBase):
    id: int
    logo_url: Optional[str] = None
    clinic_id: Optional[int] = None
    class Config:
        from_attributes = True
