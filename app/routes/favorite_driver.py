# app/routes/favorite_driver.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.favorite_driver import FavoriteDriverCreate, FavoriteDriverOut
from app.crud import favorite_driver as favorite_driver_crud
from app.database.mysql import SessionLocal

router = APIRouter(prefix="/favorites", tags=["Favorites"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FavoriteDriverOut, status_code=status.HTTP_201_CREATED)
def create_favorite_driver(payload: FavoriteDriverCreate, db: Session = Depends(get_db)):
    # Optional validations:
    if not payload.user_uid:
        raise HTTPException(status_code=400, detail="user_uid is required")
    if not payload.user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    if not payload.driver_id:
        raise HTTPException(status_code=400, detail="driver_id is required")
    fav = favorite_driver_crud.create_favorite(db, payload)
    return fav

@router.get("/user/{user_uid}", response_model=List[FavoriteDriverOut])
def list_user_favorites(user_uid: str, db: Session = Depends(get_db)):
    favs = favorite_driver_crud.list_favorites_by_user_uid(db, user_uid)
    return favs

@router.get("/{fav_id}", response_model=FavoriteDriverOut)
def get_favorite(fav_id: int, db: Session = Depends(get_db)):
    fav = favorite_driver_crud.get_favorite_by_id(db, fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return fav

@router.delete("/{fav_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(fav_id: int, db: Session = Depends(get_db)):
    deleted = favorite_driver_crud.delete_favorite_by_id(db, fav_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return
