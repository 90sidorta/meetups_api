from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models, utils
from ..schemas.users import UserResponse, UserCreate


def user_already_exists(email: str, username: str, db: Session):
    """
    Checks if user with given username or email already exists
    Args:
        email: user email
        username: user username
        db: db connection
    Raises:
        Exception if user already exists
    """
    user_email_query = db.query(models.User).filter(models.User.email == email)
    user_email = user_email_query.first()
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: '{email}' already exists!",
        )
    user_name_query = db.query(models.User).filter(models.User.username == username)
    user_name = user_name_query.first()
    if user_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with name: '{email}' already exists!",
        )


def user_create(user: UserCreate, db: Session):
    """
    Creates user in the database if username and email are not taken already
    Args:
        user: user request body
        db: db session
    Returns:
        new user data
    """
    user_already_exists(user.email, user.username, db)
    user.password = utils.hash_pass(user.password)
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {exc}"
        )
