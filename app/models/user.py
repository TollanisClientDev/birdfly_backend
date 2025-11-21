from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(64), unique=True, index=True, nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    phone = Column(String(15), unique=True, nullable=True)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

