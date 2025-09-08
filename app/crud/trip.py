from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.schemas.trip import TripCreate
from app.models.trip import TripStatus

def create_trip(db: Session, trip_data: TripCreate):
    trip = Trip(**trip_data.dict())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

def get_trip(db: Session, trip_id: int):
    return db.query(Trip).filter(Trip.id == trip_id).first()

def get_all_trips(db: Session):
    return db.query(Trip).all()
