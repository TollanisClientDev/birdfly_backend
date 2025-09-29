from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    phone = Column(String(15), unique=True, nullable=True)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    # Note: The 422 error is likely due to your Pydantic schema (in app/schemas/user.py)
    # requiring 'email' and 'phone' fields. To allow null values, update your Pydantic
    # schemas to make these fields Optional, e.g.:
    # email: Optional[str] = None
    # phone: Optional[str] = None

