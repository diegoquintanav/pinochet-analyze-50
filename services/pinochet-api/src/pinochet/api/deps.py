import logging
from typing import Any, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pinochet.database.session import SessionLocal
from pinochet.schemas.token import TokenPayload

# from pinochet.database.models.token import Token
from pinochet.settings import settings
from pydantic import ValidationError
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_str}/auth/access-token",
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


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
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # token = crud.token.get(db, id=token_data.sub)
    token = None

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return bool(token)
