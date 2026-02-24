from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class JewelerBase(BaseModel):
    name: str
    shop_name: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class JewelerCreate(JewelerBase):
    pass


class JewelerResponse(JewelerBase):
    id: int
    rating: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True