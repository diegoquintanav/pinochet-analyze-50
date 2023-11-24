from typing import Any, Optional, Union

from fastapi import APIRouter, Depends
from pinochet.api.deps import get_db
from pinochet.database.models import Victim
from pinochet.schemas.common import NoResultFound
from pinochet.schemas.victim import VictimOut
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all", response_model=list[VictimOut], status_code=201)
def get_multi_victims(
    skip: int = 0,
    limit: int = 100,
    # current models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all victims from the DB
    """

    return db.query(Victim).offset(skip).limit(limit).all()


@router.get(
    "/",
    response_model=Union[list[VictimOut], NoResultFound],
    status_code=201,
)
def get_victim_by_id_or_name(
    db: Session = Depends(get_db),
    id: Optional[int] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all victims from the DB given a name or a victim_id
    """

    q = db.query(Victim)

    if id:
        return q.where(Victim.individual_id == id).all()
    elif first_name or last_name:
        if first_name and not last_name:
            q = q.where(Victim.first_name == first_name)
        if last_name and not first_name:
            q = q.where(Victim.last_name == last_name)
        return q.all()
    else:
        query = dict(id=id, first_name=first_name, last_name=last_name)
        return NoResultFound(message="No victim found", query=query)
