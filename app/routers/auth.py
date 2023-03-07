from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import authentication
from ..database import get_db
from ..schemas.auth import AccessToken

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=AccessToken)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authentication.authenticate(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(status_code=403, detail="Incorrect username or password")

    return {
        "access_token": authentication.create_access_token(sub=user.id),  # 4
        "token_type": "bearer",
    }


@router.get("/me")
def read_users_me(current_user=Depends(authentication.get_current_user)):
    user = current_user
    return user
