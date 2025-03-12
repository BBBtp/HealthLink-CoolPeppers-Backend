from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.shemas.service import Service
from app.db.crud import service as crud

router = APIRouter()

@router.get("/", response_model=list[Service])
async def get_services(
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    clinic_id: int | None = None,
    doctor_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    services = await crud.get_services(db=db, skip=skip, limit=limit, search=search, clinic_id=clinic_id, doctor_id=doctor_id)
    return services

@router.get("/{service_id}", response_model=Service)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    db_service = await crud.get_service(db=db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service
