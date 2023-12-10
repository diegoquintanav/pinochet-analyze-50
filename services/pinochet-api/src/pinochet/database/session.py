from pinochet.settings import ApiEnvironment, settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

should_echo = settings.API_ENV in (ApiEnvironment.DEV, ApiEnvironment.TEST)
engine = create_engine(settings.db_uri, pool_pre_ping=True, echo=should_echo)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
