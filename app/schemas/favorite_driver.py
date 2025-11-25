# app/schemas/favorite_driver.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class DriverSnapshot(BaseModel):
    vehicle_make: Optional[str]
    vehicle_model: Optional[str]
    vehicle_year: Optional[int]
    license_number: Optional[str]
    rating: Optional[float]

class FavoriteDriverCreate(BaseModel):
    user_id: int
    user_uid: str
    driver_id: int
    driver_uid: Optional[str] = None
    driver_first_name: Optional[str] = None
    driver_last_name: Optional[str] = None
    driver_email: Optional[str] = None
    driver_phone: Optional[str] = None
    driver_photo_url: Optional[str] = None
    driver_status: Optional[bool] = None
    note: Optional[str] = None

class FavoriteDriverOut(FavoriteDriverCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
