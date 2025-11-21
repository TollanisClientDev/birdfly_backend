from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import hashlib
from fastapi import HTTPException, Depends
from app.database.mysql import SessionLocal
from app.utils.uid import make_uid

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(db: Session, user_data: UserCreate):
    data = user_data.dict()
    pwd = data.get("password")
    # If password is not already a 64-char hex (SHA-256), hash it
    if not (isinstance(pwd, str) and len(pwd) == 64 and all(c in "0123456789abcdef" for c in pwd.lower())):
        data["password"] = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    db_user = User(**data)
    db.add(db_user)
    db.flush()
    generated_uid = make_uid(db_user.role_id, db_user.id)
    db_user.uid = generated_uid
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_uid_or_404(uid: str, db: Session):
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with uid not found")  # pyright: ignore[reportUndefined]
    return user

def user_from_uid(uid: str, db: Session = Depends(get_db)):
    return get_user_by_uid_or_404(uid, db)

def get_user_by_email_or_phone(db: Session, email: str = None, phone: str = None):
    if email:
        return db.query(User).filter(User.email == email).first()
    if phone:
        return db.query(User).filter(User.phone == phone).first()
    return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
