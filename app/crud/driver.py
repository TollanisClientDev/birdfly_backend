# app/crud/driver.py
from sqlalchemy.orm import Session
from app import models, schemas

def create_driver(db: Session, driver_in: schemas.DriverCreate):
    db_obj = models.Driver(
        user_id=driver_in.user_id,
        license_number=driver_in.license_number,
        vehicle_number=driver_in.vehicle_number,
        vehicle_type=driver_in.vehicle_type,
        is_available=driver_in.is_available if driver_in.is_available is not None else True
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_driver_by_id(db: Session, driver_id: int):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()

def delete_driver_by_id(db: Session, driver_id: int):
    obj = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
