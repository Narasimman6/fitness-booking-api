from fastapi.testclient import TestClient
from main import app
from models import FitnessClass, Booking
from database import classes_db, bookings_db
from datetime import datetime, timedelta

client = TestClient(app)

def test_get_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_booking():
    test_class = classes_db[0]
    booking_data = {
        "class_id": test_class.id,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    
    response = client.post("/book", json=booking_data)
    assert response.status_code == 201
    assert response.json()["client_email"] == "test@example.com"
    
    # Check if available slots decreased
    updated_class = next(cls for cls in classes_db if cls.id == test_class.id)
    assert updated_class.available_slots == test_class.available_slots - 1

def test_get_bookings():
    test_email = "test@example.com"
    response = client.get(f"/bookings?email={test_email}")
    assert response.status_code == 200
    assert len(response.json()) > 0
