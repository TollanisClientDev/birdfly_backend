# app/routes/driver.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.driver import DriverCreate, DriverOut
from app.crud import driver as driver_crud, user as user_crud

router = APIRouter(prefix="/drivers", tags=["Drivers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DriverOut, status_code=status.HTTP_201_CREATED)
def create_driver(details: DriverCreate, db: Session = Depends(get_db)):
    # Optional: validate user exists
    user = user_crud.get_user(db, details.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    created = driver_crud.create_driver(db, details)
    return created

@router.get("/{driver_id}", response_model=DriverOut)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = driver_crud.get_driver_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.get("/uid/{uid}", response_model=DriverOut)
def get_driver_by_uid(uid: str, db: Session = Depends(get_db)):
    driver = driver_crud.get_driver_by_uid(db, uid)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    deleted = driver_crud.delete_driver_by_id(db, driver_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Driver not found")
    # return 204 with no content
    return
