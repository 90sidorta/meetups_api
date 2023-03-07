from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate ,db: Session = Depends(get_db)):
    try:
        user.password = utils.hash_pass(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {exc}")


@router.get("/", response_model=List[schema.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: str = ""
    ):
    users_query = db.query(models.User).filter(models.User.username.contains(search)).limit(limit).offset(skip)
    users = users_query.all()
    if users:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found!")


@router.get("/{id}", response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        single_user = db.query(models.User).filter(models.User.id == id).one()
        return single_user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id: {id} found")
