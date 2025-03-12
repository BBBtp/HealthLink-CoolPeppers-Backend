import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.db.session import get_db, Base
from app.db.models import Service

# Создание тестовой БД (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для тестовой БД
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)  # Создаем таблицы
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Удаляем таблицы после тестов


# Фикстура для тестового клиента FastAPI
@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# Тест получения списка сервисов (без фильтрации)
def test_get_services(client, test_db):
    service1 = Service(id=1, name="Service 1", description="Test service 1", price=100)
    service2 = Service(id=2, name="Service 2", description="Test service 2", price=200)

    test_db.add_all([service1, service2])
    test_db.commit()

    response = client.get("/api/v1/services/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Service 1"
    assert data[1]["name"] == "Service 2"


# Тест получения списка сервисов с фильтром по названию
def test_get_services_with_search(client, test_db):
    service1 = Service(id=1, name="Dental Cleaning", description="Teeth cleaning service", price=150)
    service2 = Service(id=2, name="X-Ray", description="Full body scan", price=300)

    test_db.add_all([service1, service2])
    test_db.commit()

    response = client.get("/api/v1/services/?search=Dental")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Dental Cleaning"


# Тест получения деталей сервиса
def test_get_service_details(client, test_db):
    service = Service(id=1, name="Consultation", description="Doctor consultation", price=50)
    test_db.add(service)
    test_db.commit()

    response = client.get("/api/v1/services/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Consultation"


# Тест получения несуществующего сервиса
def test_get_nonexistent_service(client):
    response = client.get("/api/v1/services/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"
