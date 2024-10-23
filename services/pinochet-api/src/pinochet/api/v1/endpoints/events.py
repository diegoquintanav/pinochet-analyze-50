from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from pinochet.api.deps import get_db
from pinochet.models import Event
from pinochet.schemas.event import EventOut

router = APIRouter()


@router.get("/", response_model=list[EventOut], status_code=201)
def get_multi_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all events from the DB
    """

    return db.query(Event).offset(skip).limit(limit).all()


@router.get(
    "/{event_id}",
    response_model=EventOut,
    status_code=201,
)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Get all events from the DB given an event id.
    """

    q = db.query(Event)

    event = q.where(Event.event_id == event_id).one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Item not found")

    return event
