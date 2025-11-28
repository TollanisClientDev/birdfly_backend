from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SearchItem(BaseModel):
    description: Optional[str] = None
    lat: float
    lng: float
    distance: float

class SearchCreate(BaseModel):
    user_uid: str
    data: SearchItem

class SearchOut(BaseModel):
    id: str
    user_uid: str
    description: Optional[str]
    lat: float
    lng: float
    distance: float
    created_at: datetime
