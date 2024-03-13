import logging
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pinochet import crud
from pinochet.database.models import User
from pinochet.database.session import SessionLocal
from pinochet.schemas.token import TokenPayload
from pinochet.settings import settings
from pydantic import ValidationError
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_str}/auth/token",
)

logger = logging.getLogger(__name__)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
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
