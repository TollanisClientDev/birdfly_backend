from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.user import UserCreate, UserOut, UserLogin
import hashlib
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

@router.get("/lookup", response_model=UserOut)
def get_user_by_email_or_phone(
    email: str = Query(default=None),
    phone: str = Query(default=None),
    db: Session = Depends(get_db)
):
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Must provide either email or phone.")

    user = user_crud.get_user_by_email_or_phone(db, email=email, phone=phone)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

@router.get("/uid/{uid}", response_model=UserOut)
def get_user_by_uid_or_404(uid: str, db: Session = Depends(get_db)):
    user = user_crud.user_from_uid(uid, db)
    return user

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

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Must provide either email or phone.")

    user = user_crud.get_user_by_email_or_phone(db, email=payload.email, phone=payload.phone)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # Hash incoming plaintext password using SHA-256 to match stored scheme
    incoming_hashed = hashlib.sha256(payload.password.encode("utf-8")).hexdigest()

    # Support both hashed and legacy plaintext stored passwords during transition
    if user.password not in (incoming_hashed, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {
        "id": user.id,
        "uid": user.uid,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "role_id": user.role_id,
    }
