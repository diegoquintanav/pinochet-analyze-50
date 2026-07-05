from typing import Any, Optional, Union

from fastapi import APIRouter, Depends
from pinochet.api.deps import get_db
from pinochet.models import Location
from pinochet.schemas.common import NoResultFound
from pinochet.schemas.location import LocationOut
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all", response_model=list[LocationOut], status_code=200)
def get_multi_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all locations from the DB.
    """

    return db.query(Location).offset(skip).limit(limit).all()


@router.get(
    "/",
    response_model=Union[list[LocationOut], NoResultFound],
    status_code=200,
)
def get_location_by_id_or_name(
    db: Session = Depends(get_db),
    id: Optional[int] = None,
    location_name: Optional[str] = None,
) -> Any:
    """
    Get all locations from the DB given a name or a location_id.
    """

    q = db.query(Location)

    if id is not None:
        return q.where(Location.location_id == id).all()
    elif location_name:
        q = q.where(Location.location_name == location_name)
        return q.all()
    else:
        query = dict(id=id, location_name=location_name)
        return NoResultFound(message="No location found", query=query)
