from typing import Any, Optional, Union

from fastapi import APIRouter, Depends
from pinochet.api.deps import get_db
from pinochet.models import Location
from pinochet.schemas.common import NoResultFound
from pinochet.schemas.location import LocationOut
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all", response_model=list[LocationOut], status_code=201)
def get_multi_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all locations from the DB
    """

    return db.query(Location).offset(skip).limit(limit).all()


@router.get(
    "/",
    response_model=Union[list[LocationOut], NoResultFound],
    status_code=201,
)
def get_location_by_id_or_name(
    db: Session = Depends(get_db),
    id: Optional[int] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Any:
    """
    Get all locations from the DB given a name or a location_id
    """

    q = db.query(Location)

    if id:
        return q.where(Location.individual_id == id).all()
    elif first_name or last_name:
        if first_name and not last_name:
            q = q.where(Location.first_name == first_name)
        if last_name and not first_name:
            q = q.where(Location.last_name == last_name)
        return q.all()
    else:
        query = dict(id=id, first_name=first_name, last_name=last_name)
        return NoResultFound(message="No location found", query=query)
