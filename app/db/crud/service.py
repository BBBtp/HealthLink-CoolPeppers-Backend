from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.service import Service, clinic_service_association
from fastapi import HTTPException

async def get_services(db: AsyncSession, skip: int = 0, limit: int = 100, search: str = "",
                       clinic_id: int | None = None, doctor_id: int | None = None):
    """
    Получение списка услуг с возможностью фильтрации и пагинации.

    Эта функция возвращает список услуг с возможностью фильтрации по имени услуги, клинике и врачу.
    Также поддерживает пагинацию.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - skip: int — количество записей для пропуска (по умолчанию 0).
    - limit: int — количество записей для возврата (по умолчанию 100).
    - search: str — строка для поиска по имени услуги.
    - clinic_id: int | None — уникальный идентификатор клиники для фильтрации.
    - doctor_id: int | None — уникальный идентификатор врача для фильтрации.

    Возвращает:
    - Список объектов Service — найденные услуги, соответствующие критериям поиска и фильтрации.

    Исключения:
    - HTTPException: 404 — если результаты не найдены (в зависимости от контекста).
    """
    query = select(Service)

    if search:
        query = query.filter(Service.name.ilike(f"%{search}%"))

    if clinic_id:
        query = query.join(clinic_service_association).filter(clinic_service_association.c.clinic_id == clinic_id)

    result = await db.execute(query.offset(skip).limit(limit))  # Асинхронное выполнение запроса
    services = result.scalars().all()  # Получение списка результатов

    if not services:
        raise HTTPException(status_code=404, detail="Услуги не найдены")

    return services

async def get_service(db: AsyncSession, service_id: int):
    """
    Получение услуги по её уникальному идентификатору.

    Эта функция возвращает одну услугу по её уникальному идентификатору.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - service_id: int — уникальный идентификатор услуги.

    Возвращает:
    - Объект Service — услуга с заданным идентификатором.

    Исключения:
    - HTTPException: 404 — если услуга с таким идентификатором не найдена.
    """
    query = select(Service).filter(Service.id == service_id)
    result = await db.execute(query)  # Асинхронное выполнение запроса
    service = result.scalars().first()  # Получение первого результата

    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    return service
