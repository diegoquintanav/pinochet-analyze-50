from typing import Annotated, Any, Union

import strawberry
from fastapi import Depends
from jose import jwt
from loguru import logger
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info

from pinochet import crud
from pinochet.api.deps import get_db
from pinochet.settings import ApiSettings, get_settings


@strawberry.type
class User:
    username: str
    password: str


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(
        self,
        source: Any,
        info: Info,
        settings: Annotated[ApiSettings, Depends(get_settings)],
        **kwargs,
    ) -> bool:
        request: Union[Request, WebSocket] = info.context.request

        if "Authorization" not in request.headers:
            self.message = f"{self.message}: bad header"
            return False

        authorization = request.headers.get("Authorization", "")
        token = authorization.replace("Bearer ", "")

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except (jwt.JWSError, jwt.JWTError) as e:
            logger.warning(e)
            self.message = "Invalid token"
            return False

        username: str = payload.get("sub")

        db = next(get_db())

        user = crud.user.get_by_username(db, username=username)

        if user:
            return True

        return False
