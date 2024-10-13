from typing import Optional

from pinochet.api.core.security import verify_password
from pinochet.crud.base import CRUDBase
from pinochet.models import User
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_enabled(self, user: User) -> bool:
        return user.is_enabled


user = CRUDUser(User)
