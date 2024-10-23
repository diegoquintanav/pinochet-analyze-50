from pinochet.settings import ApiEnvironment, get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Generator


def get_db() -> Generator:
    settings = get_settings()

    should_echo = (
        settings.API_ENV in (ApiEnvironment.DEV, ApiEnvironment.TEST) and False
    )
    engine = create_engine(settings.db_uri, pool_pre_ping=True, echo=should_echo)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
