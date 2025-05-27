from pydantic import BaseModel
from typing import List, Optional


class SymptomInput(BaseModel):
    symptoms: List[str]

class MatchResult(BaseModel):
    services: str

class SymptomOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True