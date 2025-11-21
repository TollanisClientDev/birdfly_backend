from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_uid = Column(String(64), index=True, nullable=True)
    plan_name = Column(String(100))
    price = Column(DECIMAL(10, 2))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    user = relationship("User")
