from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/uid/{uid}", response_model=SubscriptionOut)
def get_Subscription_by_uid(uid: str, db: Session = Depends(get_db)):
    result = subscription_crud.get_subscription_by_uid(db, uid)
    if not result:
        raise HTTPException(status_code=404, detail="Subscription details not found.")
    return result

@router.get("/", response_model=list[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    return subscription_crud.get_subscriptions(db)
