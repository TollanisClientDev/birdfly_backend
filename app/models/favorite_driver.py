# app/models/favorite_driver.py
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, JSON
from sqlalchemy import ForeignKey, Index
from app.database.mysql import Base
from sqlalchemy import Boolean

class FavoriteDriver(Base):
    __tablename__ = "favorite_drivers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user_uid = Column(String(64), nullable=False, index=True)
    driver_id = Column(BigInteger, nullable=False, index=True)
    driver_uid = Column(String(64), nullable=True)
    driver_first_name = Column(String(255), nullable=True)
    driver_last_name = Column(String(255), nullable=True)
    driver_email = Column(String(255), nullable=True)
    driver_phone = Column(String(50), nullable=True)
    driver_photo_url = Column(String(1024), nullable=True)
    driver_status = Column(Boolean, nullable=True)
    note = Column(String(512), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

# optionally, create indexes here if your ORM workflow requires explicit index declarations
Index("idx_fav_user_uid", FavoriteDriver.user_uid)
Index("idx_fav_driver_id", FavoriteDriver.driver_id)
