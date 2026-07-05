import datetime as dt
from typing import Annotated, Any, Dict

import bcrypt
from fastapi import Depends
from jose import jwt

from pinochet.settings import ApiSettings, get_settings


def create_access_token(
    data: Dict[str, Any],
    settings: Annotated[ApiSettings, Depends(get_settings)],
    expires_delta: dt.timedelta = None,
) -> str:
    """Create an access token with a subject and optional expiration date."""

    to_encode = data.copy()

    if expires_delta:
        expire = dt.datetime.now(dt.timezone.utc) + expires_delta
    else:
        expire = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )
