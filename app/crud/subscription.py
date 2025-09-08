from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate

def create_subscription(db: Session, data: SubscriptionCreate):
    sub = Subscription(**data.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def get_subscriptions(db: Session):
    return db.query(Subscription).all()
