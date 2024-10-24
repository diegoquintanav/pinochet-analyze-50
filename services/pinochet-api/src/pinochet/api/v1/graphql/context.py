from functools import cached_property
from typing import Union

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext

from pinochet.api.deps import get_current_user, get_db
from pinochet.api.v1.graphql.auth import User


class Context(BaseContext):
    @cached_property
    def user(self) -> Union["User", None]:
        db = next(get_db())

        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", "")
        token = authorization.replace("Bearer ", "")

        try:
            return get_current_user(db=db, token=token)
        except HTTPException:
            return None

    @cached_property
    def db(self) -> Union["Session", None]:
        if not self.request:
            return None

        return next(get_db())


async def get_context() -> Context:
    return Context()
