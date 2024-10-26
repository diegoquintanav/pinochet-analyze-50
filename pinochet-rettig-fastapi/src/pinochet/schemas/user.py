import datetime as dt
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: Optional[str] = None
    is_enabled: Optional[bool] = None


class UserInDB(User):
    id: int
    hashed_password: str
    created_at: dt.datetime
    updated_at: dt.datetime
    last_seen_at: dt.datetime
