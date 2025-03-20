from typing import Optional

from pydantic import BaseModel

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    photo_url: str | None = None
    rating: float

class DoctorCreate(DoctorBase):
    description: str

class Doctor(DoctorBase):
    id: int
    description: str
    experience: Optional[int] = None
    customer_count: Optional[int] = None
    reviews_count: Optional[int] = None
    class Config:
        from_attributes = True

class DoctorFavorite(BaseModel):
    message: str
