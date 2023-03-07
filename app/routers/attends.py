from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .errors import RouteErrorHandler
from .. import models, authentication
from ..schemas.auth import Attend
from ..database import get_db

router = APIRouter(prefix="/attends", tags=["Attends"], route_class=RouteErrorHandler)


@router.post("/", status_code=status.HTTP_201_CREATED)
def attend_meetup(
    attend: Attend,
    db: Session = Depends(get_db),
    user: int = Depends(authentication.get_current_user),
):
    meetup = (
        db.query(models.Meetup).filter(models.Meetup.id == attend.meetup_id).first()
    )

    if not meetup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This meetup does not exist!"
        )

    if meetup.organizer_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This is your own meetup!"
        )

    attend_query = db.query(models.Atend).filter(
        models.Atend.meetup_id == attend.meetup_id, models.Atend.user_id == user.id
    )
    already_attend = attend_query.first()

    if attend.join:
        if already_attend:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already signed up for this meetup!",
            )

        new_attend = models.Atend(meetup_id=attend.meetup_id, user_id=user.id)
        db.add(new_attend)
        db.commit()
        db.refresh(new_attend)
        return new_attend
    else:
        if not already_attend:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You did not signed up for this meetup!",
            )
        attend_query.delete()
        db.commit()
        return already_attend
