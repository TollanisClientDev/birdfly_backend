from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.crud import feedback as feedback_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FeedbackOut)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    return feedback_crud.create_feedback(db, feedback)

@router.get("/", response_model=list[FeedbackOut])
def list_feedbacks(db: Session = Depends(get_db)):
    return feedback_crud.get_feedbacks(db)
