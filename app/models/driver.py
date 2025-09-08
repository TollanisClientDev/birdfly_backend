from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.mysql import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    license_number = Column(String(100))
    vehicle_number = Column(String(50))
    vehicle_type = Column(String(50))
    is_available = Column(Boolean, default=True)

    user = relationship("User", backref="driver_profile")
