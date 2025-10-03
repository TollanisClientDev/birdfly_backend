from sqlalchemy.orm import Session
from app.models.formality import LoginFormality
from app.schemas.formality import FormalityCreate, FormalityOut

def create_formality(db: Session, formality: FormalityCreate):
    db_formality = LoginFormality(**formality.model_dump())
    db.add(db_formality)
    db.commit()
    db.refresh(db_formality)
    return db_formality

def get_formality_by_user_id(db: Session, user_id: int):
    return db.query(LoginFormality).filter(LoginFormality.user_id == user_id).first()
