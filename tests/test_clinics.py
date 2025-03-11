from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_clinics():
    response = client.get("/api/v1/clinics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_clinic_details():
    response = client.get("/api/v1/clinics/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()

def test_add_clinic_to_favorites():
    # Вам потребуется авторизация
    response = client.post("/api/v1/clinics/1/favorite", headers={"Authorization": "Bearer <token>"})
    assert response.status_code == 200
    assert response.json() == {"message": "Clinic added to favorites"}

def test_remove_clinic_from_favorites():
    # Вам потребуется авторизация
    response = client.delete("/api/v1/clinics/1/favorite", headers={"Authorization": "Bearer <token>"})
    assert response.status_code == 200
    assert response.json() == {"message": "Clinic removed from favorites"}
