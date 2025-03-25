# api/appointment_slots.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.db.session import get_db

from app.db.crud.appointment_slot import create_slot, create_slots_for_doctor, get_slots_for_doctor, get_slot_by_id
from app.shemas.appointment_slot import AppointmentSlot

router = APIRouter()

@router.get("/slots",response_model=list[AppointmentSlot])
async def get_slots_ednpoint(
        doctor_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
        Эндпоинт для получения эндпоинтов врача.

        Аргументы:
        - doctor_id: int — идентификатор врача.
        - db: AsyncSession — объект базы данных.
        """
    slots = await get_slots_for_doctor(doctor_id = doctor_id, db=db)
    return slots

@router.get("/slots/{slot_id}",response_model=AppointmentSlot)
async def get_slots_id_endpoint(
        slot_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
        Эндпоинт для получения слота записи.

        Аргументы:
        - doctor_id: int — идентификатор врача.
        - db: AsyncSession — объект базы данных.
        """
    slots = await get_slot_by_id(slot_id = slot_id, db=db)
    return slots

@router.post("/slots", response_model=AppointmentSlot)
async def create_slot_endpoint(
    doctor_id: int,
    slot_time: datetime,
    db: AsyncSession = Depends(get_db)
):
    """
    Эндпоинт для создания нового слота для врача.

    Аргументы:
    - doctor_id: int — идентификатор врача.
    - slot_time: datetime — время слота.
    - db: AsyncSession — объект базы данных.
    """
    try:
        new_slot = await create_slot(db=db, doctor_id=doctor_id, slot_time=slot_time)
        return new_slot
    except HTTPException as e:
        raise e

@router.post("/generate_slots")
async def generate_doctor_slots(
    doctor_id: int,
    start_time: datetime,
    end_time: datetime,
    db: AsyncSession = Depends(get_db)
):
    """
    Эндпоинт для генерации слотов для врача в заданном временном интервале.

    Аргументы:
    - doctor_id: int — уникальный идентификатор врача.
    - start_time: datetime — начальное время для генерации слотов.
    - end_time: datetime — конечное время для генерации слотов.
    - db: AsyncSession — объект базы данных.
    """
    try:
        # Вызов функции для создания слотов
        slots = await create_slots_for_doctor(db=db, doctor_id=doctor_id, start_time=start_time, end_time=end_time)
        return {"message": f"{len(slots)} slots created for doctor {doctor_id}"}
    except HTTPException as e:
        # Обработка ошибок (если врач не найден)
        raise e