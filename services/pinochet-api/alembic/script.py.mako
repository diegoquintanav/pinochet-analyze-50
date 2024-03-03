"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""


# revision identifiers, used by Alembic.
# template obtained from https://alembic.sqlalchemy.org/en/latest/cookbook.html#conditional-migration-elements

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}


import logging

from alembic import context, op
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

${imports if imports else ""}


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
    """schema upgrade migrations go here."""
    ${upgrades if upgrades else "pass"}


def schema_downgrades(session: Session):
    """schema downgrade migrations go here."""
    ${downgrades if downgrades else "pass"}


def data_upgrades(session: Session):
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades(session: Session):
    """Add any optional data downgrade migrations here!"""
    pass