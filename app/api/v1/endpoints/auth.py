from fastapi import APIRouter, Depends, HTTPException, Form
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.db.crud import user as crud
from app.db.crud.user import create_user
from app.db.models import User
from app.shemas.user import UserCreate, UserLogin, Token, TokenRefresh, UserBase
from app.db.session import get_db
from app.core.security import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM

router = APIRouter()


@router.post("/register", response_model=UserBase)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).filter(User.username == user.username))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
    db_user = await create_user(db, user)
    return db_user


@router.post("/login", response_model=Token)
async def login_user(username: str = Form(...),
    password: str = Form(...), db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, username, password)  # Асинхронно
    if not user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh):
    try:
        # Декодируем refresh token и проверяем его
        payload = jwt.decode(token_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        # Если в токене нет username, выбрасываем исключение
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Если refresh token еще не истек, создаем новый access и refresh токены
        access_token = create_access_token(data={"sub": username})
        refresh_token = create_refresh_token(data={"sub": username})

        return {"access_token": access_token, "refresh_token": refresh_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

