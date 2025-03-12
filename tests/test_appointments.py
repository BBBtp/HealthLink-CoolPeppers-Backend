import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import User, Appointment
from app.db.session import get_db, Base
from main import app

# Настройка тестовой базы данных (SQLite в памяти)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для создания тестовой базы данных
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)  # Создание схемы БД
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Очистка БД после теста


# Фикстура для замены зависимости get_db
@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# Фикстура для создания тестового пользователя
@pytest.fixture(scope="function")
def test_user(test_db):
    user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


# Фикстура для создания токена авторизации
@pytest.fixture(scope="function")
def auth_headers(test_user):
    from app.core.security import create_access_token
    token = create_access_token({"sub": test_user.username})
    return {"Authorization": f"Bearer {token}"}


# Тест создания записи на прием
def test_create_appointment(client, test_db, test_user, auth_headers):
    appointment_data = {"doctor_id": 1, "date": "2025-04-01T10:00:00", "service_id": 2}
    response = client.post("/appointments/", json=appointment_data, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["doctor_id"] == appointment_data["doctor_id"]
    assert data["date"] == appointment_data["date"]
    assert data["service_id"] == appointment_data["service_id"]


# Тест получения списка записей пользователя
def test_get_user_appointments(client, test_db, test_user, auth_headers):
    response = client.get("/appointments/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Тест удаления записи на прием
def test_delete_appointment(client, test_db, test_user, auth_headers):
    # Создадим запись перед тестом удаления
    appointment = Appointment(user_id=test_user.id, doctor_id=1, service_id=2)
    test_db.add(appointment)
    test_db.commit()
    test_db.refresh(appointment)

    response = client.delete(f"/appointments/{appointment.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Appointment cancelled"}

    # Проверяем, что запись удалена
    response = client.get("/appointments/", headers=auth_headers)
    assert appointment.id not in [appt["id"] for appt in response.json()]
