import enum
from abc import ABC
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional
import os

from decouple import config, Csv
from sqlalchemy.engine.url import URL


class ApiEnvironment(str, enum.Enum):
    CONTAINER_TEST = "container_test"
    CONTAINER_DEV = "container_dev"
    TEST = "test"
    DEV = "dev"
    PROD = "prod"


MISSING_ENV = ">>> API_ENV is missing or not in (test, dev, prod) <<<"
MISSING_VALUE = ">>> Missing Value <<<"
ENVIRONMENT = os.getenv("API_ENV", MISSING_ENV)


class ApiSettings(ABC):
    API_ENV: str = config("API_ENV", default=ENVIRONMENT)
    SECRET_KEY: str = config("SECRET_KEY", default=MISSING_VALUE)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POSTGRES_HOST: str = config("POSTGRES_HOST", default=MISSING_VALUE)
    POSTGRES_USER: str = config("POSTGRES_USER", default=MISSING_VALUE)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default=MISSING_VALUE)
    POSTGRES_DB: str = config("POSTGRES_DB", default=MISSING_VALUE)
    POSTGRES_PORT: int = 5432
    BACKEND_CORS_ORIGINS: list[str] = config(
        "BACKEND_CORS_ORIGINS",
        default=MISSING_VALUE,
        cast=Csv(),
    )
    SQLALCHEMY_DATABASE_URI: Optional[str] = config(
        "SQLALCHEMY_DATABASE_URI", default=MISSING_VALUE
    )
    TIMEZONE: str = "Chile/Santiago"
    PROJECT_ROOT_DIR: Path = Path(__file__).parent.parent

    @property
    def project_name(self) -> str:
        return f"Pinochet - Rettig ({self.API_ENV})"

    @property
    def db_uri(self) -> URL:
        return URL.create(
            drivername="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            database=self.POSTGRES_DB,
            port=self.POSTGRES_PORT,
        )


class ProdSettings(ApiSettings):
    pass


class DevSettings(ProdSettings):
    # Backend
    # https://fastapi.tiangolo.com/tutorial/cors/?h=cors#cors-cross-origin-resource-sharing
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    POSTGRES_HOST: str = "0.0.0.0."
    POSTGRES_USER: str = "postgres_dev"
    POSTGRES_PASSWORD: str = "dontusemeinprod"
    POSTGRES_DB: str = "pinochet_dev"
    POSTGRES_PORT: int = 5433
    SECRET_KEY: str = "dev_secret_key"


class ContainerDevSettings(DevSettings):
    POSTGRES_HOST: str = "postgis"
    POSTGRES_PORT: int = 5432


class TestSettings(DevSettings):
    POSTGRES_HOST: str = "0.0.0.0"
    POSTGRES_PORT: int = 5434
    POSTGRES_USER: str = "postgres_test"
    POSTGRES_PASSWORD: str = "postgres_password_test"
    POSTGRES_DB: str = "pinochet_test"
    SECRET_KEY: str = "test_secret_key"


class ContainerTestSettings(TestSettings):
    POSTGRES_HOST: str = "postgis-test"
    POSTGRES_PORT: int = 5432


_environment_dispatch: Dict[str, Any] = {
    ApiEnvironment.CONTAINER_TEST: ContainerTestSettings(),
    ApiEnvironment.CONTAINER_DEV: ContainerDevSettings(),
    ApiEnvironment.TEST: TestSettings(),
    ApiEnvironment.DEV: DevSettings(),
    ApiEnvironment.PROD: ProdSettings(),
}


@lru_cache()
def get_settings() -> ApiSettings:
    """Dispatch settings based on environment variable API_ENV.

    Defaults to "dev" with a warning if API_ENV is not set.
    """

    # Settings are cached
    return _environment_dispatch[ENVIRONMENT]
