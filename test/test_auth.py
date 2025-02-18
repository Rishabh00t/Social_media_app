from fastapi.testclient import TestClient
from src.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:rishabh@localhost:5432/:memory:"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

client = TestClient(app)
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEyIiwiaWQiOjIzLCJleHAiOjE3Mzg5OTE1Njh9.AoaJiMMfJh84Cj32YisROaESHGL1nRCigO2JhSOEQUs"

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_user_create():
    response = client.post("/signup", json={"username": "testuser12", "password": "TestPassword123", "email": "test12@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] and "user" in data and "Access-token" in data

def test_user_login():
    response = client.post("/login", json={"username": "testuser12", "password": "TestPassword123"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] and "user" in data and "Access_token" in data and "Refresh_token" in data


def test_user_delete():
    user_id = 23  # Ensure this user exists
    response = client.delete(f"/deleteuser/{user_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200 and response.json()["success"]

def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] and "users" in data