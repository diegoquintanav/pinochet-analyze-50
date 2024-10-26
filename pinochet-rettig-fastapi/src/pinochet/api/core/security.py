from datetime import datetime, timedelta
from typing import Annotated, Any, Dict

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext

from pinochet.settings import ApiSettings, get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: Dict[str, Any],
    settings: Annotated[ApiSettings, Depends(get_settings)],
    expires_delta: timedelta = None,
) -> str:
    """Create an access token with a subject and optional expiration date."""

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
