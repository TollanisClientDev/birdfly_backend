from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    user_id: int
    trip_id: int
    rating: int
    comment: Optional[str]

class FeedbackOut(FeedbackCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
