from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import models, utils
from ..schemas.users import UserResponse, UserCreate
from ..database import get_db
from ..services.users import user_create

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_create(user, db)


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db), limit: int = 20, skip: int = 0, search: str = ""
):
    users_query = (
        db.query(models.User)
        .filter(models.User.username.contains(search))
        .limit(limit)
        .offset(skip)
    )
    users = users_query.all()
    if users:
        return users
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found!"
    )


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        single_user = db.query(models.User).filter(models.User.id == id).one()
        return single_user
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id: {id} found"
        )
