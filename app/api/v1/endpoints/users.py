from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shemas.user import UserProfile
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserProfile)
def get_profile(
    current_user = Depends(get_current_user)  # Требуется авторизация
):
    return current_user
