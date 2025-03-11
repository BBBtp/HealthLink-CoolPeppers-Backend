from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

load_dotenv()
Base = declarative_base()

DATABASE_URL = settings.DATABASE_URL

# Создаём движок с асинхронным драйвером asyncpg
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Генератор сессий
async def get_db():
    async with SessionLocal() as session:
        yield session
