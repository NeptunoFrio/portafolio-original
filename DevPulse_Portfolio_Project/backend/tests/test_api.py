import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"

def test_create_service_and_reject_duplicate(client):
    payload = {"name": "Orders API", "url": "https://orders.example.com", "environment": "production"}
    assert client.post("/api/services", json=payload).status_code == 201
    assert client.post("/api/services", json=payload).status_code == 409

def test_down_check_creates_incident(client):
    item = client.post("/api/services", json={"name":"Billing API","url":"https://billing.example.com","environment":"staging"}).json()
    result = client.post(f"/api/services/{item['id']}/checks", json={"status":"down","latency_ms":2000,"message":"Timeout"})
    assert result.status_code == 201
    assert any(i["service_id"] == item["id"] for i in client.get("/api/incidents").json())
