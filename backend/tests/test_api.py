import os
os.environ["DATABASE_URL"] = "sqlite:///./test_airbnb.db"
os.environ["SEED_ON_STARTUP"] = "false"
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.seed.seed import seed

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
seed()
client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_listings():
    assert client.get("/listings").status_code == 200

def test_quote():
    from datetime import date, timedelta
    start = date.today() + timedelta(days=40)
    end = start + timedelta(days=3)
    r = client.get(f"/listings/2/quote?check_in={start}&check_out={end}")
    assert r.status_code == 200
    assert r.json()["nights"] == 3

def test_booking_overlap():
    from datetime import date, timedelta
    start = date.today() + timedelta(days=50)
    end = start + timedelta(days=3)
    r = client.post("/bookings", json={
        "listing_id": 2, "check_in": str(start),
        "check_out": str(end), "guests": 2
    }, headers={"X-User-Id": "3"})
    assert r.status_code == 201
    r2 = client.post("/bookings", json={
        "listing_id": 2, "check_in": str(start + timedelta(days=1)),
        "check_out": str(end + timedelta(days=1)), "guests": 2
    }, headers={"X-User-Id": "4"})
    assert r2.status_code == 409
