from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.shemas.doctor import Doctor, DoctorFavorite
from app.db.crud import doctor as crud

router = APIRouter()

@router.get("/", response_model=list[Doctor])
async def get_doctors(
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    clinic_id: int | None = None,
    service_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    doctors = await crud.get_doctors(db=db, skip=skip, limit=limit, search=search, clinic_id=clinic_id,service_id=service_id)
    return doctors

@router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    db_doctor = await crud.get_doctor(db=db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.post("/{doctor_id}/favorite", response_model=DoctorFavorite)
async def add_doctor_to_favorites(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Авторизация
):
    await crud.add_to_favorites(db=db, user_id=current_user.id, doctor_id=doctor_id)
    return {"message": "Doctor added to favorites"}

@router.delete("/{doctor_id}/favorite", response_model=DoctorFavorite)
async def remove_doctor_from_favorites(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Авторизация
):
    await crud.remove_from_favorites(db=db, user_id=current_user.id, doctor_id=doctor_id)
    return {"message": "Doctor removed from favorites"}
