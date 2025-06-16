from models import FitnessClass
from datetime import datetime, timedelta

# Initialize in-memory database
classes_db = [
    FitnessClass(
        id=1,
        name="Morning Yoga",
        date_time=(datetime.now() + timedelta(days=1)).replace(hour=8, minute=0).isoformat(),
        instructor="Alice Smith",
        available_slots=15
    ),
    FitnessClass(
        id=2,
        name="Evening Zumba",
        date_time=(datetime.now() + timedelta(days=2)).replace(hour=18, minute=30).isoformat(),
        instructor="Bob Johnson",
        available_slots=10
    ),
    FitnessClass(
        id=3,
        name="HIIT Workout",
        date_time=(datetime.now() + timedelta(days=3)).replace(hour=7, minute=0).isoformat(),
        instructor="Charlie Brown",
        available_slots=5
    ),
]

bookings_db = []
