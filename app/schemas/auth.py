from typing import Optional
from pydantic import BaseModel


class Signin(BaseModel):
    email: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Attend(BaseModel):
    meetup_id: int
    join: bool
