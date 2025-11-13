# app/routes/driver.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=schemas.DriverOut, status_code=status.HTTP_201_CREATED)
def create_driver(details: schemas.DriverCreate, db: Session = Depends(get_db)):
    # Optional: validate user exists
    user = db.query(models.User).filter(models.User.id == details.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    created = crud.create_driver(db, details)
    return created

@router.get("/{driver_id}", response_model=schemas.DriverOut)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = crud.get_driver_by_id(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_driver_by_id(db, driver_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Driver not found")
    # return 204 with no content
    return
