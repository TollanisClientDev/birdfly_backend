from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    role_id: int

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True
