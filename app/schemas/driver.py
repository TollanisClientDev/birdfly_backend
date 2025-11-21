# app/schemas/driver.py
from pydantic import BaseModel, Field
from typing import Optional


class VehicleDetails(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    type: Optional[str] = None


class DriverBase(BaseModel):
    user_id: int
    user_uid: str
    license_plate_number: Optional[str] = Field(None, alias="license_number")
    social_security_number: Optional[str] = None
    vehicle_details: Optional[VehicleDetails] = None
    is_available: Optional[bool] = True

    class Config:
        allow_population_by_field_name = True


class DriverCreate(DriverBase):
    pass


class DriverOut(DriverBase):
    id: int

    class Config(DriverBase.Config):
        from_attributes = True
