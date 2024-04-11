from typing import Annotated, Union

import strawberry
from pinochet import crud
from pinochet.api.deps import get_db


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
