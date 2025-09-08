from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, DECIMAL
from sqlalchemy.orm import relationship
from app.database.mysql import Base
import enum
from datetime import datetime

class TripStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    pickup_location = Column(String(255))
    drop_location = Column(String(255))
    fare = Column(DECIMAL(10, 2))
    distance = Column(Float)
    status = Column(Enum(TripStatus), default=TripStatus.pending)
    scheduled_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    driver = relationship("Driver")
