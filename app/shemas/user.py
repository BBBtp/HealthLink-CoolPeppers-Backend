from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # Это нужно для работы с SQLAlchemy объектами

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenRefresh(BaseModel):
    refresh_token: str

class UserProfile(UserBase):
    class Config:
        from_attributes = True
