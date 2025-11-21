from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_uid = Column(String(64), index=True, nullable=True)
    social_security_number = Column(String(255), nullable=True)
    license_plate_number = Column(String(50), nullable=True, index=True)
    vehicle_details = Column(JSON, nullable=True)
    is_available = Column(Boolean, default=True)

    user = relationship("User", backref="driver_profile")
