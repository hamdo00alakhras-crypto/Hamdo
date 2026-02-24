from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None