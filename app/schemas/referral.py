from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReferralCreate(BaseModel):
    referrer_id: int
    referred_id: int
    referral_code: str
    reward_amount: float

class ReferralOut(ReferralCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
