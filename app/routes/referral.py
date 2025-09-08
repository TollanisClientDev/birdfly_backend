from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.referral import ReferralCreate, ReferralOut
from app.crud import referral as referral_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReferralOut)
def create_referral(referral: ReferralCreate, db: Session = Depends(get_db)):
    return referral_crud.create_referral(db, referral)

@router.get("/", response_model=list[ReferralOut])
def list_referrals(db: Session = Depends(get_db)):
    return referral_crud.get_referrals(db)
