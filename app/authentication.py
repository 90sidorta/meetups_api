from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .database import get_db
from . import models, utils
from .schemas.users import UserBase
from .schemas.auth import TokenData
from .config import settings

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def authenticate(
    *,
    email: str,
    password: str,
    db: Session = Depends(get_db),
) -> Optional[UserBase]:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not utils.verify_pass(password, user.password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, exception):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        id: str = payload.get("sub")
        if id is None:
            raise exception
        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        raise exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, exception)
