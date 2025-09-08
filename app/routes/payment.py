from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.payment import PaymentCreate, PaymentOut
from app.crud import payment as payment_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return payment_crud.create_payment(db, payment)

@router.get("/", response_model=list[PaymentOut])
def list_payments(db: Session = Depends(get_db)):
    return payment_crud.get_payments(db)
