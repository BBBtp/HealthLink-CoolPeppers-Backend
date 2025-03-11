from sqlalchemy.orm import Session
from app.db.models.appointment import Appointment
from app.shemas.appointment import AppointmentCreate

def create_appointment(db: Session, appointment: AppointmentCreate, user_id: int):
    """
    Создание записи, привязанной к пользователю.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - appointment: AppointmentCreate — данные для создания записи (модель данных).
    - user_id: int — уникальный идентификатор пользователя, к которому привязывается запись.

    Возвращает:
    - Объект Appointment — созданная запись, привязанная к пользователю.
    """
    db_appointment = Appointment(**appointment.dict(), user_id=user_id)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_user_appointments(db: Session, user_id: int):
    """
    Получение всех записей для текущего пользователя.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя, для которого нужно получить записи.

    Возвращает:
    - Список объектов Appointment — все записи, принадлежащие пользователю с указанным user_id.
    """
    return db.query(Appointment).filter(Appointment.user_id == user_id).all()


def delete_appointment(db: Session, appointment_id: int, user_id: int):
    """
    Удаление записи пользователя по ее ID.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - appointment_id: int — уникальный идентификатор записи, которую нужно удалить.
    - user_id: int — уникальный идентификатор пользователя, чтобы убедиться, что запись принадлежит ему.

    Возвращает:
    - bool — True, если запись была удалена, или False, если запись не принадлежала пользователю.
    """
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment:
        if db_appointment.user_id != user_id:
            return False  # Запись не принадлежит текущему пользователю
        db.delete(db_appointment)
        db.commit()
        return True
    return False
