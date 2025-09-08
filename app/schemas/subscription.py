from pydantic import BaseModel
from datetime import datetime

class SubscriptionCreate(BaseModel):
    user_id: int
    plan_name: str
    price: float
    start_date: datetime
    end_date: datetime

class SubscriptionOut(SubscriptionCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
