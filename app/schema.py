from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class MeetupBase(BaseModel):
    title: str
    description: str
    published: bool = True
    price: Optional[int] = None
    limit: Optional[int] = None
    address: str


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool


class MeetupCreate(MeetupBase):
    pass


class UserCreate(UserBase):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    created_at: datetime
    username: str
    email: str
    
    class Config:
        orm_mode = True


class MeetupAddData(MeetupBase):
    id: int
    created_at: datetime
    organizer_id: int
    organizer: UserResponse
    
    class Config:
        orm_mode = True


class MeetupResponse(BaseModel):
    Meetup: MeetupAddData
    attend: int

    class Config:
        orm_mode = True
 

class Signin(BaseModel):
    email: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Atend(BaseModel):
    meetup_id: int
    join: bool

