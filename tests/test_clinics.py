import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.session import get_db, Base
from app.db.models import User, Clinic

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


# Тест получения списка клиник
def test_get_clinics(client, test_db):
    clinic = Clinic(id=1, name="City Hospital")
    test_db.add(clinic)
    test_db.commit()

    response = client.get("/api/v1/clinics/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "City Hospital"


# Тест получения информации о конкретной клинике
def test_get_clinic_details(client, test_db):
    clinic = Clinic(id=1, name="City Hospital")
    test_db.add(clinic)
    test_db.commit()

    response = client.get("/api/v1/clinics/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "City Hospital"


# Тест ошибки при запросе несуществующей клиники
def test_get_nonexistent_clinic(client):
    response = client.get("/api/v1/clinics/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Clinic not found"


# Тест добавления клиники в избранное
def test_add_clinic_to_favorites(auth_client, test_db):
    clinic = Clinic(id=1, name="City Hospital")
    test_db.add(clinic)
    test_db.commit()

    response = auth_client.post("/api/v1/clinics/1/favorite")

    assert response.status_code == 200
    assert response.json()["message"] == "Clinic added to favorites"
