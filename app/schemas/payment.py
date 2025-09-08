from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    user_id: int
    trip_id: int
    amount: float
    method: str
    status: Optional[str] = "pending"

class PaymentOut(PaymentCreate):
    id: int
    paid_at: Optional[datetime]

    class Config:
        from_attributes = True
