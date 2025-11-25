# app/crud/favorite_driver.py
from sqlalchemy.orm import Session
from app.models.favorite_driver import FavoriteDriver
from app.schemas.favorite_driver import FavoriteDriverCreate ,FavoriteDriverOut

def create_favorite(db: Session, payload: FavoriteDriverCreate):
    # Optionally prevent duplicates: don't create if same user -> same driver exists
    existing = db.query(FavoriteDriver).filter(
        FavoriteDriver.user_id == payload.user_id,
        FavoriteDriver.driver_id == payload.driver_id
    ).first()
    if existing:
        return existing

    obj = FavoriteDriver(
        user_id = payload.user_id,
        user_uid = payload.user_uid,
        driver_id = payload.driver_id,
        driver_uid = payload.driver_uid,
        driver_first_name = payload.driver_first_name,
        driver_last_name = payload.driver_last_name,
        driver_email = payload.driver_email,
        driver_phone = payload.driver_phone,
        driver_photo_url = payload.driver_photo_url,
        driver_status = payload.driver_status,
        note = payload.note
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_favorites_by_user_uid(db: Session, user_uid: str):
    return db.query(FavoriteDriver).filter(FavoriteDriver.user_uid == user_uid).order_by(FavoriteDriver.created_at.desc()).all()

def get_favorite_by_id(db: Session, fav_id: int):
    return db.query(FavoriteDriver).filter(FavoriteDriver.id == fav_id).first()

def delete_favorite_by_id(db: Session, fav_id: int):
    obj = db.query(FavoriteDriver).filter(FavoriteDriver.id == fav_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
