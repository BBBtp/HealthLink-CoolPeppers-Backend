from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.appointment import Appointment
from app.shemas.appointment import AppointmentCreate


async def create_appointment(db: AsyncSession, appointment: AppointmentCreate, user_id: int):
    """
    Создание записи, привязанной к пользователю.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - appointment: AppointmentCreate — данные для создания записи (модель данных).
    - user_id: int — уникальный идентификатор пользователя, к которому привязывается запись.

    Возвращает:
    - Объект Appointment — созданная запись, привязанная к пользователю.
    """
    db_appointment = Appointment(**appointment.dict(), user_id=user_id)
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment


async def get_user_appointments(db: AsyncSession, user_id: int):
    """
    Получение всех записей для текущего пользователя.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - user_id: int — уникальный идентификатор пользователя, для которого нужно получить записи.

    Возвращает:
    - Список объектов Appointment — все записи, принадлежащие пользователю с указанным user_id.
    """
    query = select(Appointment).filter(Appointment.user_id == user_id)
    result = await db.execute(query)
    appointments = result.scalars().all()
    return appointments


async def delete_appointment(db: AsyncSession, appointment_id: int, user_id: int):
    """
    Удаление записи пользователя по ее ID.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - appointment_id: int — уникальный идентификатор записи, которую нужно удалить.
    - user_id: int — уникальный идентификатор пользователя, чтобы убедиться, что запись принадлежит ему.

    Возвращает:
    - bool — True, если запись была удалена, или False, если запись не принадлежала пользователю.
    """
    query = select(Appointment).filter(Appointment.id == appointment_id)
    result = await db.execute(query)
    db_appointment = result.scalars().first()

    if db_appointment:
        if db_appointment.user_id != user_id:
            return False  # Запись не принадлежит текущему пользователю
        await db.delete(db_appointment)
        await db.commit()
        return True
    return False
