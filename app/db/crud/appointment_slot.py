# crud/appointment_slot.py
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import AppointmentSlot, Doctor
from app.db.models.appointment_slot import SlotStatus
from fastapi import HTTPException


async def create_slot(db: AsyncSession, doctor_id: int, slot_time: datetime) -> AppointmentSlot:
    """
    Создание нового слота для врача.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - doctor_id: int — уникальный идентификатор врача.
    - slot_time: datetime — время слота.

    Возвращает:
    - Новый объект AppointmentSlot.
    """
    # Проверяем, существует ли врач с таким doctor_id
    doctor = await db.execute(select(Doctor).filter(Doctor.id == doctor_id))
    doctor = doctor.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Проверяем, доступен ли этот слот для врача
    existing_slot = await db.execute(
        select(AppointmentSlot).filter(
            AppointmentSlot.doctor_id == doctor_id,
            AppointmentSlot.slot_time == slot_time
        )
    )
    existing_slot = existing_slot.scalar_one_or_none()

    if existing_slot:
        raise HTTPException(status_code=400, detail="Slot already exists")

    # Создание нового слота
    new_slot = AppointmentSlot(doctor_id=doctor_id, slot_time=slot_time)
    db.add(new_slot)
    await db.commit()
    await db.refresh(new_slot)

    return new_slot


def generate_slots_for_doctor(doctor_id: int, start_time: datetime, end_time: datetime, interval_minutes: int = 30):
    """
    Генерация слотов для врача в заданном временном интервале.

    Аргументы:
    - doctor_id: int — уникальный идентификатор врача.
    - start_time: datetime — начальное время для генерации слотов.
    - end_time: datetime — конечное время для генерации слотов.
    - interval_minutes: int — интервал между слотами в минутах (по умолчанию 30 минут).

    Возвращает:
    - Список объектов AppointmentSlot — сгенерированные слоты.
    """
    current_time = start_time
    slots = []
    while current_time < end_time:
        slot = AppointmentSlot(doctor_id=doctor_id, slot_time=current_time,status=SlotStatus.available.value)
        slots.append(slot)
        current_time += timedelta(minutes=interval_minutes)
    return slots


async def create_slots_for_doctor(db: AsyncSession, doctor_id: int, start_time: datetime, end_time: datetime, interval_minutes: int = 30):
    """
    Генерация и сохранение слотов для врача в базе данных.

    Аргументы:
    - db: AsyncSession — объект базы данных для выполнения запроса.
    - doctor_id: int — уникальный идентификатор врача.
    - start_time: datetime — начальное время для генерации слотов.
    - end_time: datetime — конечное время для генерации слотов.
    - interval_minutes: int — интервал между слотами в минутах.

    Возвращает:
    - Список добавленных слотов.
    """
    # Проверяем, существует ли врач с таким doctor_id
    doctor = await db.execute(select(Doctor).filter(Doctor.id == doctor_id))
    doctor = doctor.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Генерация слотов для врача
    slots = generate_slots_for_doctor(doctor_id, start_time, end_time, interval_minutes)

    # Добавляем слоты в базу данных
    db.add_all(slots)
    await db.commit()

    return slots


async def get_slots_for_doctor(db: AsyncSession, doctor_id: int):
    """
       Список слотов выбранного врача

       Аргументы:
       - db: AsyncSession — объект базы данных для выполнения запроса.
       - doctor_id: int — уникальный идентификатор врача.

       Возвращает:
       - Список добавленных слотов.
       """
    query = select(AppointmentSlot).filter(AppointmentSlot.doctor_id == doctor_id, AppointmentSlot.status == SlotStatus.available.value)
    results = await db.execute(query)
    slots = results.scalars().all()
    return slots

async def get_slot_by_id(db: AsyncSession, slot_id: int):
    """
           Список слотов выбранного врача

           Аргументы:
           - db: AsyncSession — объект базы данных для выполнения запроса.
           - doctor_id: int — уникальный идентификатор врача.

           Возвращает:
           - Список добавленных слотов.
           """
    query = select(AppointmentSlot).filter(AppointmentSlot.id == slot_id)
    result = await db.execute(query)
    slot = result.scalars().first()
    return slot