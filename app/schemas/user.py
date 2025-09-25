from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    role_id: int

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True

