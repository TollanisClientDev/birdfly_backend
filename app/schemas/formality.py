from pydantic import BaseModel
from typing import Optional

class FormalityCreate(BaseModel):
    user_id: int
    notification: bool
    location: bool
    referral_code: Optional[str]
    terms_and_conditions: bool
    formality_done: bool

class FormalityOut(FormalityCreate):
    id: int

    class Config:
        from_attributes = True