from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.driver import DriverCreate, DriverOut
from app.crud import driver as driver_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DriverOut)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    return driver_crud.create_driver(db, driver)

@router.get("/{driver_id}", response_model=DriverOut)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = driver_crud.get_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.get("/", response_model=list[DriverOut])
def list_drivers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return driver_crud.get_all_drivers(db, skip, limit)

@router.delete("/{driver_id}", response_model=DriverOut)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = driver_crud.delete_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
