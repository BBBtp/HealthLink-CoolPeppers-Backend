from sqlalchemy import Column, Integer, String, Text

from app.db.session import Base


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(Text, nullable=True)
