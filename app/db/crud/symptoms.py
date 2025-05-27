from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Symptom


async def get_all_symptoms(db: AsyncSession):
    result = await db.execute(select(Symptom))
    return result.scalars().all()