from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate

def create_subscription(db: Session, data: SubscriptionCreate):
    sub = Subscription(**data.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def get_subscription_by_uid(db: Session, user_uid: str):
    subscription = db.query(Subscription).filter(Subscription.user_uid == user_uid).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

def get_subscriptions(db: Session):
    return db.query(Subscription).all()
