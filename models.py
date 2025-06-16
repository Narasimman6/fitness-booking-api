from pydantic import BaseModel, EmailStr
from typing import Optional

class FitnessClass(BaseModel):
    id: int
    name: str
    date_time: str  # ISO format datetime string
    instructor: str
    available_slots: int
    max_slots: int = 20

class Booking(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    booking_time: str  # ISO format datetime string
