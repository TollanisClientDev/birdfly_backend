from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/uid/{uid}", response_model=FeedbackOut)
def get_feedback_by_uid(uid: str, db: Session = Depends(get_db)):
    feedback = feedback_crud.get_feedback_by_uid(db, uid)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.get("/", response_model=list[FeedbackOut])
def list_feedbacks(db: Session = Depends(get_db)):
    return feedback_crud.get_feedbacks(db)
