from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TripCreate(BaseModel):
    user_id: int
    driver_id: int
    pickup_location: str
    drop_location: str
    fare: float
    distance: float
    scheduled_time: Optional[datetime] = None

class TripOut(TripCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
