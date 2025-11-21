from sqlalchemy.orm import Session
from app.models.formality import LoginFormality
from app.schemas.formality import FormalityCreate, FormalityOut

def create_formality(db: Session, formality: FormalityCreate):
    formality_data = formality.model_dump()
    # Map 'uid' from schema to 'user_uid' in model
    formality_data["user_uid"] = formality_data.pop("uid")
    db_formality = LoginFormality(**formality_data)
    db.add(db_formality)
    db.commit()
    db.refresh(db_formality)
    return db_formality

def get_formality_by_user_id(db: Session, user_id: int):
    return db.query(LoginFormality).filter(LoginFormality.user_id == user_id).first()

def get_formality_by_uid(db: Session, uid: str):
    return db.query(LoginFormality).filter(LoginFormality.user_uid == uid).first()