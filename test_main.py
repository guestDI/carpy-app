import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

def test_upload_file():
    with open("test_file.txt", "wb") as f:
        f.write(b"sample data")

    with open("test_file.txt", "rb") as file:
        response = client.post("/car-works/upload/", files={"file": file})
    
    assert response.status_code == 200
    assert response.json()["filename"] == "test_file.txt"

def test_get_stats():
    response = client.get("/car-works/stats/", params={"month": 9, "year": 2024})
    assert response.status_code == 200
    assert "total_expense" in response.json()

# def test_maintenance_reminders():
#     # mock db in future
#     response = client.get("/car-works/")
#     assert response.status_code == 200
