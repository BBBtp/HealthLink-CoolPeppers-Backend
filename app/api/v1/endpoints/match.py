from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.symptoms import get_all_symptoms
from app.db.session import get_db
from app.db.crud import service as crud_service
from app.core.gpt import get_services_by_symptoms
from app.shemas.match import SymptomInput, MatchResult, SymptomOut

router = APIRouter()

@router.post("/match-services", response_model=MatchResult)
async def match_services(payload: SymptomInput, db: AsyncSession = Depends(get_db)):
    services = await crud_service.get_services(db)
    services_data = [{"name": s.name, "description": s.description} for s in services]
    result = get_services_by_symptoms(payload.symptoms, services_data)
    return {"services": result}


@router.get("/symptoms/", response_model=list[SymptomOut])
async def read_all_symptoms(db: AsyncSession = Depends(get_db)):
    symptoms = await get_all_symptoms(db)
    return symptoms