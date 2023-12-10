from typing import Any, Optional

from fastapi import APIRouter, Depends
from pinochet.api.deps import get_db
from pinochet.database.models import Event
from pinochet.schemas.event import EventOut
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all", response_model=list[EventOut], status_code=201)
def get_multi_events(
    skip: int = 0,
    limit: int = 100,
    # current models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all events from the DB
    """

    return db.query(Event).offset(skip).limit(limit).all()


@router.get(
    "/",
    response_model=EventOut,
    status_code=201,
)
def get_victim_by_id_or_name(
    db: Session = Depends(get_db),
    id: Optional[int] = None,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all events from the DB given a name or a event id
    """

    q = db.query(Event)

    if id:
        return q.where(Event.individual_id == id).all()

    return None
