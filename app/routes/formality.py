from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import formality as formality_crud
from app.schemas.formality import FormalityOut, FormalityCreate
from app.database.mysql import SessionLocal

router = APIRouter(prefix="/formalities", tags=["Formalities"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FormalityOut)
def create_formality(formality: FormalityCreate, db: Session = Depends(get_db)):
    existing = formality_crud.get_formality_by_user_id(db, formality.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Formalities already submitted for this user.")
    return formality_crud.create_formality(db, formality)

@router.get("/{user_id}", response_model=FormalityOut)
def get_formality(user_id: int, db: Session = Depends(get_db)):
    result = formality_crud.get_formality_by_user_id(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Formalities not found.")
    return result

@router.get("/uid/{uid}", response_model=FormalityOut)
def get_formality_by_uid(uid: str, db: Session = Depends(get_db)):
    result = formality_crud.get_formality_by_uid(db, uid)
    if not result:
        raise HTTPException(status_code=404, detail="Formalities not found.")
    return result
