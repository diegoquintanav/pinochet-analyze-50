import typer

from loguru import logger

from typing import Annotated
from fastapi import Depends


from pinochet.settings import get_settings, ApiSettings, ApiEnvironment

from sqlalchemy.orm import Session, DeclarativeBase


app = typer.Typer()


def recreate_db_cmd(
    base: DeclarativeBase,
    session: Session,
    settings: Annotated[ApiSettings, Depends(get_settings)],
) -> None:
    assert (
        not settings.API_ENV == ApiEnvironment.DEV
    ), "Refresh DB is only allowed in development mode"

    logger.info("Dropping tables")
    base.metadata.drop_all(bind=session.bind)
    logger.info("Creating tables")
    base.metadata.create_all(bind=session.bind)


@app.command()
def recreate_db() -> None:
    """Initialize the database."""

    from pinochet.db import SessionLocal

    session = SessionLocal()

    from pinochet import Base

    recreate_db_cmd(Base, session)


if __name__ == "__main__":
    print("Daniel Lopez")
