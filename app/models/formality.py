from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database.mysql import Base

class LoginFormality(Base):
    __tablename__ = "login_formalities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    notification = Column(Boolean, default=False)
    location = Column(Boolean, default=False)
    referral_code = Column(String(100), nullable=True)
    terms_and_conditions = Column(Boolean, default=False)
    formality_done = Column(Boolean, default=False)
