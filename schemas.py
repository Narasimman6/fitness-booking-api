from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClassSchema(BaseModel):
    id: int
    name: str
    date_time: str
    instructor: str
    available_slots: int
    
    class Config:
        orm_mode = True

class BookingCreateSchema(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingSchema(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    booking_time: str
    class_name: Optional[str] = None
    class_time: Optional[str] = None
    
    class Config:
        orm_mode = True
