from pydantic import BaseModel

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
    clinic_id: int
    doctor_id: int | None = None

    class Config:
        from_attributes = True
