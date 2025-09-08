from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class SearchItem(BaseModel):
    query: str
    type: Literal["pickup", "drop"]
    timestamp: datetime

class SearchDataCreate(BaseModel):
    user_id: int
    search: SearchItem
