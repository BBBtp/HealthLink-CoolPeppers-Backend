import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.session import get_db, Base
from app.db.models import User, Doctor

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


# Фикстура для авторизованного пользователя
@pytest.fixture(scope="function")
def auth_client(client, test_db):
    from app.core.security import create_access_token
    user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    test_db.add(user)
    test_db.commit()

    token = create_access_token(data={"sub": user.username})
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


# Тест получения списка докторов
def test_get_doctors(client, test_db):
    doctor = Doctor(id=1,first_name="Test", last_name="Dr. Smith", clinic_id=1)
    test_db.add(doctor)
    test_db.commit()

    response = client.get("/doctors/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["last_name"] == "Dr. Smith"


# Тест получения конкретного доктора
def test_get_doctor(client, test_db):
    doctor = Doctor(id=1, first_name="Test", last_name="Dr. Smith", clinic_id=1)
    test_db.add(doctor)
    test_db.commit()

    response = client.get("/doctors/1")

    assert response.status_code == 200
    assert response.json()["last_name"] == "Dr. Smith"


# Тест получения несуществующего доктора
def test_get_nonexistent_doctor(client):
    response = client.get("/doctors/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"


# Тест добавления доктора в избранное
def test_add_doctor_to_favorites(auth_client, test_db):
    doctor = Doctor(id=1, first_name="Test", last_name="Dr. Smith", clinic_id=1)
    test_db.add(doctor)
    test_db.commit()

    response = auth_client.post("/doctors/1/favorite")

    assert response.status_code == 200
    assert response.json()["message"] == "Doctor added to favorites"


