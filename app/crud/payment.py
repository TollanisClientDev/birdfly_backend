from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate

def create_payment(db: Session, payment_data: PaymentCreate):
    payment = Payment(**payment_data.dict())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def get_payment_by_uid(db: Session, user_uid: str):
    payment = db.query(Payment).filter(Payment.user_uid == user_uid).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

def get_payments(db: Session):
    return db.query(Payment).all()
