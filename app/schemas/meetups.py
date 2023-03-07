from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from .users import UserResponse


class MeetupBase(BaseModel):
    title: str
    description: str
    published: bool = True
    price: Optional[int] = None
    limit: Optional[int] = None
    address: str


class MeetupCreate(MeetupBase):
    pass


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
