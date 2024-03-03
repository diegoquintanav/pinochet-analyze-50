from typing import Annotated

from fastapi import APIRouter, Depends
from pinochet.api.deps import get_current_active_user
from pinochet.schemas import User

router = APIRouter()


@router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
