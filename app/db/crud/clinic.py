from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.clinic import Clinic
from app.shemas.clinic import ClinicCreate


async def get_clinics(db: AsyncSession, skip: int = 0, limit: int = 100, search: str = ""):
    """
    Получение списка клиник с возможностью пагинации и поиска.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - skip: int (по умолчанию 0) — количество пропущенных записей для пагинации.
    - limit: int (по умолчанию 100) — максимальное количество записей для возвращения.
    - search: str (по умолчанию "") — строка для поиска в названии клиники.

    Возвращает:
    - Список клиник, соответствующих критериям поиска и пагинации.
    """
    query = select(Clinic).filter(Clinic.name.ilike(f"%{search}%")).offset(skip).limit(limit)
    result = await db.execute(query)
    clinics = result.scalars().all()
    return clinics


async def get_clinic(db: AsyncSession, clinic_id: int):
    """
    Получение информации о клинике по её ID.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии для выполнения запроса.
    - clinic_id: int — уникальный идентификатор клиники.

    Возвращает:
    - Объект Clinic, если клиника найдена, иначе None.
    """
    query = select(Clinic).filter(Clinic.id == clinic_id)
    result = await db.execute(query)
    clinic = result.scalars().first()
    return clinic


async def create_clinic(db: AsyncSession, clinic: ClinicCreate):
    """
    Создание новой клиники в базе данных.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии для выполнения запроса.
    - clinic: ClinicCreate — данные для создания клиники (модель данных).

    Возвращает:
    - Созданный объект Clinic, который был добавлен в базу данных.
    """
    db_clinic = Clinic(**clinic.dict())
    db.add(db_clinic)
    await db.commit()
    await db.refresh(db_clinic)
    return db_clinic


async def add_to_favorites(db: AsyncSession, user_id: int, clinic_id: int):
    """
    Добавление клиники в избранное для пользователя.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя.
    - clinic_id: int — уникальный идентификатор клиники.

    Возвращает:
    - None (пока не реализована логика).
    """
    pass


async def remove_from_favorites(db: AsyncSession, user_id: int, clinic_id: int):
    """
    Удаление клиники из избранного пользователя.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя.
    - clinic_id: int — уникальный идентификатор клиники.

    Возвращает:
    - None (пока не реализована логика).
    """
    pass
