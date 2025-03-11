from sqlalchemy.orm import Session
from app.db.models.user import User
from app.shemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate) -> User:
    """
    Создает нового пользователя в базе данных.

    Эта функция хеширует пароль пользователя, создаёт новый объект пользователя
    и сохраняет его в базе данных.

    Аргументы:
    - db: Session — объект сессии базы данных.
    - user: UserCreate — объект с данными для создания пользователя.

    Возвращает:
    - User: объект пользователя, который был создан в базе данных.

    Исключения:
    - Если пользователь с таким именем или email уже существует, выбрасывается ошибка HTTPException.

    Пример:
    >>> create_user(db, user_data)
    User(id=1, username='johndoe', email='john@example.com', ...)
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Проверяет учетные данные пользователя и аутентифицирует его.

    Эта функция ищет пользователя по имени и проверяет, соответствует ли пароль
    введенному значению.

    Аргументы:
    - db: Session — объект сессии базы данных.
    - username: str — имя пользователя.
    - password: str — пароль пользователя.

    Возвращает:
    - User: объект пользователя, если аутентификация успешна.
    - None: если аутентификация не удалась (неправильный логин или пароль).

    Пример:
    >>> authenticate_user(db, 'johndoe', 'password123')
    User(id=1, username='johndoe', email='john@example.com', ...)
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Получает пользователя по его ID.

    Эта функция ищет пользователя по его уникальному идентификатору в базе данных.

    Аргументы:
    - db: Session — объект сессии базы данных.
    - user_id: int — уникальный идентификатор пользователя.

    Возвращает:
    - User: объект пользователя, если найден.
    - None: если пользователь с таким ID не найден.

    Пример:
    >>> get_user_by_id(db, 1)
    User(id=1, username='johndoe', email='john@example.com', ...)
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Получает пользователя по имени.

    Эта функция ищет пользователя по его имени в базе данных.

    Аргументы:
    - db: Session — объект сессии базы данных.
    - username: str — имя пользователя.

    Возвращает:
    - User: объект пользователя, если найден.
    - None: если пользователь с таким именем не найден.

    Пример:
    >>> get_user_by_username(db, 'johndoe')
    User(id=1, username='johndoe', email='john@example.com', ...)
    """
    return db.query(User).filter(User.username == username).first()
