from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut
from app.crud import subscription as subscription_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SubscriptionOut)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    return subscription_crud.create_subscription(db, subscription)

@router.get("/", response_model=list[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    return subscription_crud.get_subscriptions(db)
