from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .errors import RouteErrorHandler
from .. import models, schema, authentication
from ..database import get_db

router = APIRouter(
    prefix="/attends",
    tags=["Attends"],
    route_class=RouteErrorHandler
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def attend_meetup(
    atend: schema.Atend,
    db: Session = Depends(get_db),
    user: int = Depends(authentication.get_current_user)
    ):

    meetup = db.query(models.Meetup).filter(models.Meetup.id == atend.meetup_id).first()

    if not meetup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This meetup does not exist!")

    if meetup.organizer_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This is your own meetup!")


    atend_query = db.query(models.Atend).filter(
        models.Atend.meetup_id == atend.meetup_id,
        models.Atend.user_id == user.id
        )
    already_atend = atend_query.first()

    if atend.join:
        if already_atend:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already signed up for this meetup!")

        new_atend = models.Atend(meetup_id=atend.meetup_id, user_id=user.id)
        db.add(new_atend)
        db.commit()
        db.refresh(new_atend)
        return new_atend
    else:
        if not already_atend:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You did not signed up for this meetup!")
        atend_query.delete()
        db.commit()
        return already_atend
        
