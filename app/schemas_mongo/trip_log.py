from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class GPSPoint(BaseModel):
    lat: float
    lng: float
    timestamp: datetime

class TripLogCreate(BaseModel):
    trip_id: int
    driver_id: int
    user_id: int
    route: List[GPSPoint]

class TripLogAppend(BaseModel):
    trip_id: int
    new_point: GPSPoint
