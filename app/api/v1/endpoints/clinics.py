from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.crud import clinic as crud
from app.db.models import User
from app.db.session import get_db
from app.shemas.clinic import Clinic, ClinicFavorite

router = APIRouter()


@router.get("/", response_model=list[Clinic])
def get_clinics(skip: int = 0, limit: int = 100, search: str = "", db: Session = Depends(get_db)):
    clinics = crud.get_clinics(db=db, skip=skip, limit=limit, search=search)
    return clinics


@router.get("/{clinic_id}", response_model=Clinic)
def get_clinic(clinic_id: int, db: Session = Depends(get_db)):
    db_clinic = crud.get_clinic(db=db, clinic_id=clinic_id)
    if db_clinic is None:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return db_clinic


@router.post("/{clinic_id}/favorite", response_model=ClinicFavorite)
def add_clinic_to_favorites(clinic_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user())):
    # Вызовем функцию для добавления в избранное
    crud.add_to_favorites(db=db, user_id=user_id, clinic_id=clinic_id)
    return {"message": "Clinic added to favorites"}


@router.delete("/{clinic_id}/favorite", response_model=ClinicFavorite)
def remove_clinic_from_favorites(clinic_id: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(get_current_user())):
    # Вызовем функцию для удаления из избранного
    crud.remove_from_favorites(db=db, user_id=current_user.id, clinic_id=clinic_id)
    return {"message": "Clinic removed from favorites"}
