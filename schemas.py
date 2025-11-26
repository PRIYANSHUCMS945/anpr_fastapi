from pydantic import BaseModel
from datetime import datetime

class LicensePlateBase(BaseModel):
    image_name: str
    plate_text: str | None = None

class LicensePlateCreate(LicensePlateBase):
    pass

class LicensePlateOut(LicensePlateBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
