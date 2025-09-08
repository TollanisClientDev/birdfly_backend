from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.trip import TripCreate, TripOut
from app.crud import trip as trip_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TripOut)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    return trip_crud.create_trip(db, trip)

@router.get("/{trip_id}", response_model=TripOut)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = trip_crud.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.get("/", response_model=list[TripOut])
def list_trips(db: Session = Depends(get_db)):
    return trip_crud.get_all_trips(db)
