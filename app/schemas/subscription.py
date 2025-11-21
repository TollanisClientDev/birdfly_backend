from pydantic import BaseModel
from datetime import datetime

class SubscriptionCreate(BaseModel):
    user_id: int
    user_uid: str
    plan_name: str
    price: float
    start_date: datetime
    end_date: datetime

class SubscriptionOut(SubscriptionCreate):
    id: int
    is_active: bool
    user_uid: str
    class Config:
        from_attributes = True
