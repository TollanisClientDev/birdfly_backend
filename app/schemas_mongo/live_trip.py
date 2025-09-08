from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class LiveTripUpdate(BaseModel):
    trip_id: int
    user_id: int
    driver_id: int
    status: Literal[
        "assigned", 
        "reached_pickup", 
        "picked_up", 
        "en_route", 
        "completed", 
        "cancelled"
    ]
    last_updated: datetime