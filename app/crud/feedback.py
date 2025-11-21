from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

def create_feedback(db: Session, feedback_data: FeedbackCreate):
    feedback = Feedback(**feedback_data.dict())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

def get_feedback_by_uid(db: Session, user_uid: str):
    feedback = db.query(Feedback).filter(Feedback.user_uid == user_uid).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

def get_feedbacks(db: Session):
    return db.query(Feedback).all()
