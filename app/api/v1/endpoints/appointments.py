from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.shemas.appointment import Appointment, AppointmentCreate
from app.db.crud import appointment as crud


router = APIRouter()

@router.post("/", response_model=Appointment)
def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_appointment = crud.create_appointment(db=db, appointment=appointment_data,user_id=current_user.id)
    return new_appointment

@router.get("/", response_model=list[Appointment])
def get_user_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_appointments(db=db, user_id=current_user.id)

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = crud.delete_appointment(db=db, appointment_id=appointment_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment cancelled"}
