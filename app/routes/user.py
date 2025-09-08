from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.user import UserCreate, UserOut
from app.crud import user as user_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_crud.get_users(db, skip, limit)

@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
