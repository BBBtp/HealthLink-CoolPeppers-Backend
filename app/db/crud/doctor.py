from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.crud.favorites import add_to_favorites, remove_from_favorites
from app.db.models.doctor import Doctor
from app.db.models.favorites import FavoriteType
from app.db.models.service import service_doctor_association, Service


async def get_doctors(db: AsyncSession, skip: int = 0, limit: int = 100, search: str = "", clinic_id: int | None = None,service_id: int | None = None):
    """
    Получение списка врачей с возможностью фильтрации по имени, клинике и пагинации.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии для выполнения запроса.
    - skip: int (по умолчанию 0) — количество пропущенных записей для пагинации.
    - limit: int (по умолчанию 100) — максимальное количество записей для возвращения.
    - search: str (по умолчанию "") — строка для поиска по фамилии врача.
    - clinic_id: int | None (по умолчанию None) — уникальный идентификатор клиники для фильтрации по клинике.
    - service_id: int | None (по умолчанию None) — уникальный идентификатор услуги для фильтрации по услуге.

    Возвращает:
    - Список объектов Doctor — врачи, соответствующие критериям поиска, фильтрации и пагинации.
    """
    query = select(Doctor)

    if search:
        query = query.filter(Doctor.last_name.ilike(f"%{search}%"))

    if clinic_id:
        query = query.filter(Doctor.clinic_id == clinic_id)

    if service_id:
        query = query.join(service_doctor_association).join(Service).filter(Service.id == service_id)
    result = await db.execute(query)
    doctors = result.scalars().all()
    return doctors


async def get_doctor(db: AsyncSession, doctor_id: int):
    """
    Получение информации о враче по его ID.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - doctor_id: int — уникальный идентификатор врача.

    Возвращает:
    - Объект Doctor, если врач найден, иначе None.
    """
    query = select(Doctor).filter(Doctor.id == doctor_id)
    result = await db.execute(query)
    doctor = result.scalars().first()
    return doctor


async def add_doctor_to_favorites(db: AsyncSession, user_id: int, doctor_id: int):
    """
    Добавление врача в избранное для пользователя.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя.
    - doctor_id: int — уникальный идентификатор врача.

    """
    return await add_to_favorites(db, user_id, doctor_id, FavoriteType.DOCTOR)


async def remove_doctor_from_favorites(db: AsyncSession, user_id: int, doctor_id: int):
    """
    Удаление врача из избранного пользователя.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя.
    - doctor_id: int — уникальный идентификатор врача.

    """
    return await remove_from_favorites(db, user_id, doctor_id, FavoriteType.DOCTOR)
