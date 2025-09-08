from sqlalchemy.orm import Session
from app.models.referral import Referral
from app.schemas.referral import ReferralCreate

def create_referral(db: Session, data: ReferralCreate):
    referral = Referral(**data.dict())
    db.add(referral)
    db.commit()
    db.refresh(referral)
    return referral

def get_referrals(db: Session):
    return db.query(Referral).all()
