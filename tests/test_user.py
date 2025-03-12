import pytest
from fastapi.testclient import TestClient
from main import app
from app.db.models import User
from app.db.session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создание тестовой БД (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для тестовой БД
@pytest.fixture(scope="function")
def test_db():
    from app.db.session import Base
    Base.metadata.create_all(bind=engine)  # Создание таблиц
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Удаление таблиц после тестов


# Фикстура для тестового клиента FastAPI
@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# Фикстура для создания тестового пользователя и токена
@pytest.fixture(scope="function")
def auth_headers(test_db):
    from app.core.security import create_access_token
    user = User(id=1, email="test@example.com", password_hash="hashedpassword", is_active=True)
    test_db.add(user)
    test_db.commit()

    token = create_access_token(data={"sub": user.email})
    return {"Authorization": f"Bearer {token}"}


# Тест получения профиля авторизованного пользователя
def test_get_profile(client, test_db, auth_headers):
    response = client.get("/api/v1/users/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


# Тест получения профиля без авторизации
def test_get_profile_unauthorized(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401
