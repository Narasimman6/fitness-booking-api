from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from models import FitnessClass, Booking
from database import classes_db, bookings_db
from schemas import ClassSchema, BookingCreateSchema, BookingSchema
from utils import convert_timezone
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fitness Studio Booking API")

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/classes", response_model=List[ClassSchema])
def get_classes(timezone: str = "IST"):
    """Get all upcoming fitness classes with timezone conversion"""
    try:
        upcoming_classes = [
            cls for cls in classes_db 
            if datetime.fromisoformat(cls.date_time) > datetime.now()
        ]
        
        # Convert timezone for each class
        converted_classes = []
        for cls in upcoming_classes:
            converted_cls = cls.dict()
            converted_cls['date_time'] = convert_timezone(cls.date_time, "IST", timezone)
            converted_classes.append(converted_cls)
            
        return converted_classes
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching classes"
        )

@app.post("/book", response_model=BookingSchema, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreateSchema):
    """Create a new booking"""
    try:
        # Find the class
        class_to_book = next(
            (cls for cls in classes_db if cls.id == booking.class_id), 
            None
        )
        
        if not class_to_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
            
        # Check available slots
        if class_to_book.available_slots <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No available slots for this class"
            )
            
        # Check if class is in the past
        class_time = datetime.fromisoformat(class_to_book.date_time)
        if class_time < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot book past classes"
            )
            
        # Check if user already booked this class
        existing_booking = next(
            (b for b in bookings_db 
             if b.class_id == booking.class_id and b.client_email == booking.client_email),
            None
        )
        
        if existing_booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already booked this class"
            )
            
        # Create booking
        new_booking = Booking(
            id=len(bookings_db) + 1,
            class_id=booking.class_id,
            client_name=booking.client_name,
            client_email=booking.client_email,
            booking_time=datetime.now().isoformat()
        )
        
        # Update available slots
        class_to_book.available_slots -= 1
        
        # Add to database
        bookings_db.append(new_booking)
        
        return new_booking
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating booking"
        )

@app.get("/bookings", response_model=List[BookingSchema])
def get_bookings(email: str):
    """Get all bookings for a specific email"""
    try:
        user_bookings = [b for b in bookings_db if b.client_email == email]
        
        # Enrich with class information
        enriched_bookings = []
        for booking in user_bookings:
            enriched = booking.dict()
            class_info = next(
                (cls for cls in classes_db if cls.id == booking.class_id),
                None
            )
            if class_info:
                enriched['class_name'] = class_info.name
                enriched['class_time'] = class_info.date_time
            enriched_bookings.append(enriched)
            
        return enriched_bookings
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching bookings"
        )
