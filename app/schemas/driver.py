# app/schemas/driver.py
from pydantic import BaseModel
from typing import Optional

class DriverCreate(BaseModel):
    user_id: int
    license_number: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    is_available: Optional[bool] = True

class DriverOut(DriverCreate):
    id: int

    class Config:
        from_attributes = True
