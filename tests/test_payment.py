import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import User, Payment
from app.db.session import get_db, Base
from main import app

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


# Тест создания платежа
def test_create_payment(auth_client, test_db):
    payment_data = {"amount": 500, "currency": "USD", "description": "Test Payment"}

    response = auth_client.post("/api/v1/payments/create", json=payment_data)

    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 500
    assert data["currency"] == "USD"
    assert data["description"] == "Test Payment"


# Тест подтверждения платежа
def test_confirm_payment(auth_client, test_db):
    user = test_db.query(User).filter(User.username == "testuser").first()
    payment = Payment(id=1, payment_url="/test/", amount=500, status="pending")
    test_db.add(payment)
    test_db.commit()

    payment_confirm_data = {"payment_id": 1, "status": "confirmed"}

    response = auth_client.post("/api/v1/payments/confirm", json=payment_confirm_data)

    assert response.status_code == 200
    assert response.json()["message"] == "Payment status updated"


# Тест подтверждения несуществующего платежа
def test_confirm_nonexistent_payment(auth_client):
    payment_confirm_data = {"payment_id": 999, "status": "confirmed"}

    response = auth_client.post("/api/v1/payments/confirm", json=payment_confirm_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"
