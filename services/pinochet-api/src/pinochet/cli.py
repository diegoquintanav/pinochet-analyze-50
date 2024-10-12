import typer

from loguru import logger


from pinochet.settings import get_settings, ApiEnvironment

from sqlalchemy.orm import Session, DeclarativeBase


app = typer.Typer(no_args_is_help=True)

settings = get_settings()


def recreate_db_cmd(
    base: DeclarativeBase,
    session: Session,
) -> None:
    assert (
        not settings.API_ENV == ApiEnvironment.DEV
    ), "Refresh DB is only allowed in development mode"

    logger.info("Dropping tables")
    base.metadata.drop_all(bind=session.bind)
    logger.info("Creating tables")
    base.metadata.create_all(bind=session.bind)


@app.callback()
def callback():
    # to display a command even if ii is only one
    # https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback
    pass


@app.command(help="Drops and recreates the database. Only allowed in development mode.")
def recreate_db() -> None:
    """Initialize the database."""

    from pinochet.db import get_db

    session = next(get_db())

    from pinochet.base import Base

    recreate_db_cmd(Base, session)


if __name__ == "__main__":
    print("Daniel Lopez")
