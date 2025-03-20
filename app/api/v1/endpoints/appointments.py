from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.db.models import User, AppointmentSlot
from app.db.models.appointment_slot import SlotStatus
from app.db.session import get_db
from app.shemas.appointment import Appointment, AppointmentCreate
from app.db.crud import appointment as crud

router = APIRouter()

@router.post("/", response_model=Appointment)
async def create_appointment(
    clinic_id: int,
    doctor_id: int,
    service_id: int,
    date_time: datetime,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверяем, доступен ли выбранный слот для врача
    slot = await db.execute(
        select(AppointmentSlot).filter(
            AppointmentSlot.doctor_id == doctor_id,
            AppointmentSlot.slot_time == date_time,
            AppointmentSlot.status == SlotStatus.available.value
        )
    )
    slot = slot.scalar_one_or_none()

    if not slot:
        raise HTTPException(status_code=400, detail="Selected slot is not available")

    # Создание записи и обновление статуса слота на "booked"
    appointment_data = AppointmentCreate(
        clinic_id=clinic_id,
        doctor_id=doctor_id,
        service_id=service_id,
        date_time=date_time,
    )
    new_appointment = await crud.create_appointment(db=db, appointment=appointment_data, user_id=current_user.id, slot_id=slot.id)

    slot.status = SlotStatus.booked
    db.add(slot)
    await db.commit()

    return new_appointment


@router.get("/", response_model=list[Appointment])
async def get_user_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Получаем записи с учетом статуса
    appointments = await crud.get_user_appointments(db=db, user_id=current_user.id)
    return appointments

@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Удаляем запись
    success = await crud.delete_appointment(db=db, appointment_id=appointment_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found or cannot be deleted")
    return {"message": "Appointment cancelled"}
