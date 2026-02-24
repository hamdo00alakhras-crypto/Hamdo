from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from database import Base


class Jeweler(Base):
    __tablename__ = "jewelers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    shop_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())