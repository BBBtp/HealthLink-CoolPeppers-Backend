from pydantic import BaseModel
from typing import Optional

class ClinicBase(BaseModel):
    name: str
    address: str
    logo_url: Optional[str] = None

class ClinicCreate(ClinicBase):
    description: str
    rating: Optional[float] = None

class Clinic(ClinicBase):
    id: int
    description: str
    rating: float
    metro: Optional[str] = None
    price: Optional[int] = None
    work_time: Optional[str] = None
    year_foundation: Optional[int] = None
    customers_count: Optional[int] = None
    reviews_count: Optional[int] = None
    class Config:
        orm_mode = True

class ClinicFavorite(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
