# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.crud import user as crud
from app.db.models import User
from app.db.session import get_db

# Секретный ключ для подписи JWT токенов
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes


def get_password_hash(password: str) -> str:
    """
    Хеширует пароль с использованием алгоритма PBKDF2.

    Эта функция используется для хеширования паролей перед их сохранением в базе данных.
    Она генерирует уникальный хеш для каждого пароля, что повышает безопасность.

    Аргументы:
    - password: str — строка, представляющая пароль пользователя.

    Возвращает:
    - str — хешированный пароль, который будет сохранен в базе данных.

    Пример:
    >>> get_password_hash("my_secure_password")
    'pbkdf2_sha256$260000$9v...'
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли переданный пароль с хешированным значением.

    Эта функция используется для проверки введенного пароля пользователя при логине.
    Она сравнивает введенный пароль с хешированным значением в базе данных.

    Аргументы:
    - plain_password: str — строка, представляющая пароль, введенный пользователем.
    - hashed_password: str — строка, представляющая ранее сохраненный хешированный пароль.

    Возвращает:
    - bool — True, если пароль совпадает с хешем, иначе False.

    Пример:
    >>> verify_password("my_secure_password", 'pbkdf2_sha256$260000$9v...')
    True
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Функция для создания access токена"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Функция для создания refresh токена"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Функция для получения текущего пользователя на основе токена"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = crud.get_user_by_username(db, username=username)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
