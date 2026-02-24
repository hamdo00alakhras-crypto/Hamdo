from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    dob = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())