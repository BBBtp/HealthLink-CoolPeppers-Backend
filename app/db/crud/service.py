from sqlalchemy.orm import Session
from app.db.models.service import Service
from fastapi import HTTPException


def get_services(db: Session, skip: int = 0, limit: int = 100, search: str = "", clinic_id: int | None = None,
                 doctor_id: int | None = None):
    """
    Получение списка услуг с возможностью фильтрации и пагинации.

    Эта функция возвращает список услуг с возможностью фильтрации по имени услуги, клинике и врачу.
    Также поддерживает пагинацию.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
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
    query = db.query(Service)

    if search:
        query = query.filter(Service.name.ilike(f"%{search}%"))

    if clinic_id:
        query = query.filter(Service.clinic_id == clinic_id)

    if doctor_id:
        query = query.filter(Service.doctor_id == doctor_id)

    services = query.offset(skip).limit(limit).all()

    if not services:
        raise HTTPException(status_code=404, detail="Услуги не найдены")

    return services


def get_service(db: Session, service_id: int):
    """
    Получение услуги по её уникальному идентификатору.

    Эта функция возвращает одну услугу по её уникальному идентификатору.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - service_id: int — уникальный идентификатор услуги.

    Возвращает:
    - Объект Service — услуга с заданным идентификатором.

    Исключения:
    - HTTPException: 404 — если услуга с таким идентификатором не найдена.
    """
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    return service
