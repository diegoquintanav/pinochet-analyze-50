from typing import Any

from pydantic import BaseModel


class BaseMsg(BaseModel):
    detail: str


class NoResultFound(BaseMsg):
    query: Any
    detail: str = "No results found"
