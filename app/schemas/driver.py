from pydantic import BaseModel
from typing import Optional

class DriverCreate(BaseModel):
    user_id: int
    license_number: str
    vehicle_number: str
    vehicle_type: str

class DriverOut(BaseModel):
    id: int
    user_id: int
    license_number: str
    vehicle_number: str
    vehicle_type: str
    is_available: bool

    class Config:
        from_attributes = True
