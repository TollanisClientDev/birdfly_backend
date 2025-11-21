from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.mysql import Base
import enum

class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_uid = Column(String(64), index=True, nullable=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    amount = Column(DECIMAL(10, 2))
    method = Column(String(50))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    paid_at = Column(DateTime)

    user = relationship("User")
    trip = relationship("Trip")
