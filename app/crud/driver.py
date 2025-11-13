# app/crud/driver.py
from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.schemas.driver import DriverCreate

def create_driver(db: Session, driver_in: DriverCreate):
    db_obj = Driver(
        user_id=driver_in.user_id,
        license_plate_number=driver_in.license_plate_number,
        social_security_number=driver_in.social_security_number,
        vehicle_details=driver_in.vehicle_details.dict(exclude_none=True) if driver_in.vehicle_details else None,
        is_available=driver_in.is_available if driver_in.is_available is not None else True,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_driver_by_id(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.id == driver_id).first()

def delete_driver_by_id(db: Session, driver_id: int):
    obj = db.query(Driver).filter(Driver.id == driver_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
