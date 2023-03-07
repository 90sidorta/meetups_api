from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserCreate(UserBase):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    confirm_password: Optional[str]
    old_email: Optional[EmailStr]
    new_email: Optional[EmailStr]
    old_password: Optional[str]
    new_password: Optional[str]
