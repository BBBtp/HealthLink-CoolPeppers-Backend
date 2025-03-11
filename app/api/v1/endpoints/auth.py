from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.crud import user as crud
from app.db.models import User
from app.shemas.user import UserCreate, UserLogin, Token, TokenRefresh
from app.db.session import get_db
from app.core.security import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/register", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
    return crud.create_user(db, user)


@router.post("/login", response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=Token)
def refresh_token(token_data: TokenRefresh):
    # Логика обновления токена (если он валиден, выдаем новый)
    return {"access_token": "new_access_token", "refresh_token": "new_refresh_token"}
