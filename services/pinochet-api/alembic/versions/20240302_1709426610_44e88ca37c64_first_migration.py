"""first migration

does nothing

Revision ID: 44e88ca37c64
Revises: None
Create Date: 2024-03-02 21:43:30.975397

"""

# revision identifiers, used by Alembic.
# template obtained from https://alembic.sqlalchemy.org/en/latest/cookbook.html#conditional-migration-elements
# ruff: noqa: E402
# flake8: noqa: E402

revision = "44e88ca37c64"
down_revision = None

import logging

from alembic import op
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

# ---------------------------------------------------------------------------- #
#                                logging config                                #
# ---------------------------------------------------------------------------- #

logger = logging.getLogger("alembic.runtime.revision")

# ---------------------------------------------------------------------------- #
#                              tables definitions                              #
# ---------------------------------------------------------------------------- #

# MigrationBase = declarative_base()

# -------------------------------- new tables -------------------------------- #


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
    pass


def schema_downgrades(session: Session):
    """Schema downgrade migrations go here."""
    pass


def data_upgrades(session: Session):
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades(session: Session):
    """Add any optional data downgrade migrations here!"""
    pass
