from typing import List
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .errors import RouteErrorHandler
from .. import models, authentication
from ..database import get_db
from ..schemas.meetups import MeetupAddData, MeetupCreate, MeetupResponse

router = APIRouter(prefix="/meetups", tags=["Meetups"], route_class=RouteErrorHandler)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MeetupAddData)
def create_meetup(
    meetup: MeetupCreate,
    db: Session = Depends(get_db),
    user: int = Depends(authentication.get_current_user),
):
    new_meetup = models.Meetup(organizer_id=user.id, **meetup.dict())
    db.add(new_meetup)
    db.commit()
    db.refresh(new_meetup)
    return new_meetup


@router.get("/{id}", response_model=MeetupResponse)
def get_meetup(id: int, db: Session = Depends(get_db)):
    single_meetup = (
        db.query(models.Meetup, func.count(models.Atend.meetup_id).label("attend"))
        .join(models.Atend, models.Atend.meetup_id == models.Meetup.id, isouter=True)
        .group_by(models.Meetup.id)
        .filter(models.Meetup.id == id)
        .first()
    )
    if single_meetup:
        return single_meetup
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No meetup with id: {id} found!"
    )


@router.get("/", response_model=List[MeetupResponse])
def get_meetups(
    mine: bool = False,
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: str = "",
):
    meetups_query = (
        db.query(models.Meetup, func.count(models.Atend.meetup_id).label("attend"))
        .join(models.Atend, models.Atend.meetup_id == models.Meetup.id, isouter=True)
        .group_by(models.Meetup.id)
        .filter(models.Meetup.title.contains(search))
        .limit(limit)
        .offset(skip)
    )
    meetups = meetups_query.all()
    if meetups:
        return meetups
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No meetups found!"
    )


@router.put("/{id}", response_model=MeetupAddData)
def update_meetup(
    id: int,
    meetup: MeetupCreate,
    db: Session = Depends(get_db),
    user: int = Depends(authentication.get_current_user),
):
    updated_meetup_query = db.query(models.Meetup).filter(models.Meetup.id == id)
    updated_meetup = updated_meetup_query.first()
    if updated_meetup:
        if updated_meetup.organizer_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cannot modify other user meetup!",
            )

        updated_meetup_query.update(meetup.dict(), synchronize_session=False)
        db.commit()
        return updated_meetup
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No meetup with id: {id} found!"
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meetup(
    id: int,
    db: Session = Depends(get_db),
    user: int = Depends(authentication.get_current_user),
):
    deleted_meetup_query = db.query(models.Meetup).filter(models.Meetup.id == id)
    deleted_meetup = deleted_meetup_query.first()
    if deleted_meetup:
        if deleted_meetup.organizer_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cannot delete other user meetup!",
            )
        deleted_meetup_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"No meetup with id: {id} found!"
    )
