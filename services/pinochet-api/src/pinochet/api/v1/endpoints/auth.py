from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pinochet.api.deps import get_db, login_helper
from pinochet.schemas import Token
from sqlalchemy.orm import Session
from pinochet.settings import ApiSettings, get_settings

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[ApiSettings, Depends(get_settings)],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    token = await login_helper(
        username=form_data.username,
        password=form_data.password,
        db=db,
        settings=settings,
    )

    return token
