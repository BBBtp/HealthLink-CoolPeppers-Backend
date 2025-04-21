import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL_ALEMBIC: str = os.getenv('DATABASE_URL_ALEMBIC')
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
    CLOUDNAME: int = os.getenv("CLOUDNAME")
    API_KEY: str = os.getenv("API_KEY")
    API_SECRET: str = os.getenv("API_SECRET")
    SECURE: bool = os.getenv("SECURE")
    YA_API_KEY: str = os.getenv("YA_API_KEY")
    YA_FOLDER_ID: str = os.getenv("YA_FOLDER_ID")

settings = Settings()
