import logging
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from pinochet import crud
from pinochet.api.core import create_access_token
from pinochet.models import User
from pinochet.db import get_db
from pinochet.schemas import Token
from pinochet.schemas.token import TokenPayload
from pinochet.settings import (
    ApiSettings,
    get_settings,
)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

logger = logging.getLogger(__name__)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
    settings: ApiSettings = Depends(get_settings),
) -> User:
    """Get the current user from the token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        username: str = payload.get("sub")

    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from e

    user = crud.user.get_by_username(db, username=username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Same as get_current_user but checks if the user is active."""

    if not crud.user.is_enabled(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def is_token_valid(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
    settings: ApiSettings = Depends(get_settings),
) -> bool:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e

    token = crud.token.get(db, id=token_data.sub)

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return bool(token)


async def login_helper(
    username: str,
    password: str,
    db: Session,
    settings: Annotated[ApiSettings, Depends(get_settings)],
) -> Token:
    user = crud.user.authenticate(
        db=db,
        username=username,
        password=password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
        settings=settings,
    )

    return Token(access_token=access_token, token_type="bearer")
