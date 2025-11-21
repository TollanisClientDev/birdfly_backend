from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: Optional[str] = None
    password: str
    phone: Optional[str] = None
    role_id: int

class UserOut(BaseModel):
    id: int
    uid: Optional[str]
    first_name: str
    last_name: Optional[str]
    email: Optional[str] = None
    phone: Optional[str] = None
    role_id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str