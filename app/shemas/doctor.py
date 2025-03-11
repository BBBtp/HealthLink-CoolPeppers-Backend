from pydantic import BaseModel

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    photo_url: str
    rating: float

class DoctorCreate(DoctorBase):
    description: str

class Doctor(DoctorBase):
    id: int
    description: str

    class Config:
        from_attributes = True

class DoctorFavorite(BaseModel):
    message: str
