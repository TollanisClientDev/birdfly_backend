from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.schemas.driver import DriverCreate

def create_driver(db: Session, driver_data: DriverCreate):
    driver = Driver(**driver_data.dict())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver

def get_driver(db: Session, driver_id: int):
    return db.query(Driver).filter(Driver.id == driver_id).first()

def get_all_drivers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Driver).offset(skip).limit(limit).all()

def delete_driver(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver:
        db.delete(driver)
        db.commit()
    return driver
