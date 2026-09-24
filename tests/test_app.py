import pytest
import routes
from app import app
import database

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db))
    monkeypatch.setattr(routes, "get_connection", database.get_connection)
    database.init_db()

    app.config["TESTING"] = True

    with app.test_client() as client:
        routes.TOKENS.clear()
        yield client

def login(client):
    client.post("/api/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "secret123"
    })
    response = client.post("/api/login", json={
        "email": "test@example.com",
        "password": "secret123"
    })
    return response.get_json()["token"]

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

def test_register_and_login(client):
    client.post("/api/register", json={
        "name": "Rahul",
        "email": "rahul@example.com",
        "password": "password123"
    })
    response = client.post("/api/login", json={
        "email": "rahul@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()

def test_add_transaction(client):
    token = login(client)
    response = client.post(
        "/api/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "transaction_type": "expense",
            "category": "Food",
            "amount": 250,
            "description": "Lunch",
            "transaction_date": "2026-09-24"
        }
    )
    assert response.status_code == 201

def test_unauthorized_transactions(client):
    response = client.get("/api/transactions")
    assert response.status_code == 401
