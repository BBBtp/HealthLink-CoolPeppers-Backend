from sqlalchemy.orm import Session
from app.db.models.clinic import Clinic
from app.shemas.clinic import ClinicCreate

def get_clinics(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    """
    Получение списка клиник с возможностью пагинации и поиска.

    Аргументы:
    - db: Session — объект базы данных для выполнения запросов.
    - skip: int (по умолчанию 0) — количество пропущенных записей для пагинации.
    - limit: int (по умолчанию 100) — максимальное количество записей для возвращения.
    - search: str (по умолчанию "") — строка для поиска в названии клиники.

    Возвращает:
    - Список клиник, соответствующих критериям поиска и пагинации.
    """
    return db.query(Clinic).filter(Clinic.name.ilike(f"%{search}%")).offset(skip).limit(limit).all()


def get_clinic(db: Session, clinic_id: int):
    """
    Получение информации о клинике по её ID.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - clinic_id: int — уникальный идентификатор клиники.

    Возвращает:
    - Объект Clinic, если клиника найдена, иначе None.
    """
    return db.query(Clinic).filter(Clinic.id == clinic_id).first()


def create_clinic(db: Session, clinic: ClinicCreate):
    """
    Создание новой клиники в базе данных.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - clinic: ClinicCreate — данные для создания клиники (модель данных).

    Возвращает:
    - Созданный объект Clinic, который был добавлен в базу данных.
    """
    db_clinic = Clinic(**clinic.dict())
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic


def add_to_favorites(db: Session, user_id: int, clinic_id: int):
    """
    Добавление клиники в избранное для пользователя.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя.
    - clinic_id: int — уникальный идентификатор клиники.

    Возвращает:
    - None (пока не реализована логика).
    """
    pass


def remove_from_favorites(db: Session, user_id: int, clinic_id: int):
    """
    Удаление клиники из избранного пользователя.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя.
    - clinic_id: int — уникальный идентификатор клиники.

    Возвращает:
    - None (пока не реализована логика).
    """
    pass
