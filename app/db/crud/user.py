from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.shemas.user import UserCreate, UserBase
from app.core.hashing import get_password_hash, verify_password
from fastapi import HTTPException

async def create_user(db: AsyncSession, user: UserCreate) -> UserBase:
    """
    Создает нового пользователя в базе данных.

    Эта функция хеширует пароль пользователя, создаёт новый объект пользователя
    и сохраняет его в базе данных.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - user: UserCreate — объект с данными для создания пользователя.

    Возвращает:
    - User: объект пользователя, который был создан в базе данных.

    Исключения:
    - Если пользователь с таким именем или email уже существует, выбрасывается ошибка HTTPException.
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
    await db.commit()
    await db.refresh(db_user)

    return UserBase.from_orm(db_user)

async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    """
    Проверяет учетные данные пользователя и аутентифицирует его.

    Эта функция ищет пользователя по имени и проверяет, соответствует ли пароль
    введенному значению.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - username: str — имя пользователя.
    - password: str — пароль пользователя.

    Возвращает:
    - User: объект пользователя, если аутентификация успешна.
    - None: если аутентификация не удалась (неправильный логин или пароль).
    """
    query = select(User).filter(User.username == username)
    result = await db.execute(query)  # Асинхронное выполнение запроса
    user = result.scalars().first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Получает пользователя по его ID.

    Эта функция ищет пользователя по его уникальному идентификатору в базе данных.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - user_id: int — уникальный идентификатор пользователя.

    Возвращает:
    - User: объект пользователя, если найден.
    - None: если пользователь с таким ID не найден.
    """
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)  # Асинхронное выполнение запроса
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """
    Получает пользователя по имени.

    Эта функция ищет пользователя по его имени в базе данных.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - username: str — имя пользователя.

    Возвращает:
    - User: объект пользователя, если найден.
    - None: если пользователь с таким именем не найден.
    """
    query = select(User).filter(User.username == username)
    result = await db.execute(query)  # Асинхронное выполнение запроса
    return result.scalars().first()
