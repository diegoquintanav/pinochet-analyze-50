from typing import Annotated, Any, Union

import strawberry
from fastapi.exceptions import HTTPException
from loguru import logger
from pinochet import crud
from pinochet.api.deps import get_current_user, get_db
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info


@strawberry.type
class User:
    username: str
    password: str


@strawberry.type
class LoginSuccess:
    user: User


@strawberry.type
class LoginError:
    message: str


LoginResult = Annotated[
    Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
]


@strawberry.type
class Mutation:
    @strawberry.field
    async def login(self, username: str, password: str) -> LoginResult:
        db = get_db()

        user = crud.user.authenticate(
            db=db,
            username=username,
            password=password,
        )

        if not user:
            return LoginError(message="Incorrect username or password")

        return LoginSuccess(user=user)


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context.request

        if "Authorization" in request.headers:
            authorization = self.request.headers.get("Authorization", "")
            logger.debug(f"{authorization=}")
            token = authorization.replace("Bearer ", "")
            logger.debug(f"{token=}")

            try:
                db = next(get_db())
                if get_current_user(db=db, token=token):
                    return True
            except HTTPException:
                return False

        return False
