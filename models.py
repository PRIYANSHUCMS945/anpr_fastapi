from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class LicensePlate(Base):
    __tablename__ = "license_plates"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    plate_text = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
