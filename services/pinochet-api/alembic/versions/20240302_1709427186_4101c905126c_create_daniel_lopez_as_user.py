"""create daniel lopez as user

Revision ID: 4101c905126c
Revises: 44e88ca37c64
Create Date: 2024-03-02 21:53:06.608607

"""

# revision identifiers, used by Alembic.
# template obtained from https://alembic.sqlalchemy.org/en/latest/cookbook.html#conditional-migration-elements
# ruff: noqa: E402
# flake8: noqa: E402

revision = "4101c905126c"
down_revision = "44e88ca37c64"


import datetime as dt
import logging

from alembic import op
from pinochet.database.time import utcnow
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column

# ---------------------------------------------------------------------------- #
#                                logging config                                #
# ---------------------------------------------------------------------------- #

logger = logging.getLogger("alembic.runtime.revision")

# ---------------------------------------------------------------------------- #
#                              tables definitions                              #
# ---------------------------------------------------------------------------- #

MigrationBase = declarative_base()


class User(MigrationBase):
    __tablename__ = "user"
    __table_args__ = {"schema": "api"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)  # fmt: skip
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=utcnow())  # fmt: skip
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=utcnow())  # fmt: skip
    last_seen_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=utcnow())  # fmt: skip


# ------------------ existing tables needed for consistency ------------------ #


# ---------------------------------------------------------------------------- #
#                            migrations definitions                            #
# ---------------------------------------------------------------------------- #


def upgrade():
    bind: Connection = op.get_bind()
    session = Session(bind=bind)

    logger.info("Begin schema upgrades")
    schema_upgrades(session)

    logger.info("Begin data upgrades")
    data_upgrades(session)

    logger.info("Finished upgrades")


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    logger.info("Begin data downgrades")
    data_downgrades(session)

    logger.info("Begin schema downgrades")
    schema_downgrades(session)

    logger.info("Finished downgrades")


def schema_upgrades(session: Session):
    """Schema upgrade migrations go here."""
    MigrationBase.metadata.create_all(bind=session.bind)


def schema_downgrades(session: Session):
    """Schema downgrade migrations go here."""
    MigrationBase.metadata.drop_all(bind=session.bind)


def data_upgrades(session: Session):
    """Add any optional data upgrade migrations here!"""

    from pinochet.api.core.security import get_password_hash

    daniel_lopez = User(
        email="daniel.lopez@rettig.cl",
        username="daniel.lopez",
        hashed_password=get_password_hash("rettig"),
    )

    logger.info(f"Adding user {daniel_lopez.username} ({daniel_lopez.email})")
    session.add(daniel_lopez)
    session.commit()


def data_downgrades(session: Session):
    """Add any optional data downgrade migrations here!"""

    daniel_lopez = session.query(User).filter_by(email="daniel.lopez@rettig.cl").first()
    if daniel_lopez:
        logger.info(f"Deleting user {daniel_lopez.username} ({daniel_lopez.email})")
        session.delete(daniel_lopez)
        session.commit()
