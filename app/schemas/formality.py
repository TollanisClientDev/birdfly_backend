from pydantic import BaseModel, Field
from typing import Optional

class FormalityCreate(BaseModel):
    user_id: int
    user_uid: str
    notification: bool
    location: bool
    referral_code: Optional[str] = None
    terms_and_conditions: bool
    formality_done: bool

class FormalityOut(BaseModel):
    id: int
    user_id: int
    user_uid: str
    notification: bool
    location: bool
    referral_code: Optional[str] = None
    terms_and_conditions: bool
    formality_done: bool
    
    class Config:
        from_attributes = True
        populate_by_name = True