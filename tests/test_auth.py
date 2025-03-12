import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.session import get_db, Base
from app.db.models import User

# Подключаем тестовую базу данных SQLite (в памяти)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для тестовой БД
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)  # Создание таблиц
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Очистка после тестов


# Фикстура для тестового клиента FastAPI
@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# Тест регистрации пользователя
def test_register_user(client):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "securepassword", "is_active": True,
                 "is_admin": False}
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


# Тест регистрации с дублирующим именем пользователя
def test_register_duplicate_user(client, test_db):
    # Добавляем пользователя вручную
    user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    test_db.add(user)
    test_db.commit()

    user_data = {"username": "testuser", "email": "test2@example.com", "password": "securepassword", "is_active": True,
                 "is_admin": False}
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Имя пользователя уже занято"


# Тест входа пользователя
def test_login_user(client, test_db):
    # Добавляем пользователя вручную
    user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    test_db.add(user)
    test_db.commit()

    login_data = {"username": "testuser", "password": "securepassword"}
    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# Тест входа с неверными данными
def test_login_invalid_user(client):
    login_data = {"username": "wronguser", "password": "wrongpassword"}
    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверные учетные данные"


# Тест обновления токена
def test_refresh_token(client):
    token_data = {"refresh_token": "valid_refresh_token"}
    response = client.post("/auth/refresh", json=token_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
