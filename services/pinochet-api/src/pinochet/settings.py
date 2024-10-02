import enum
from abc import ABC
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional


from pydantic import DirectoryPath, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class ApiEnvironment(str, enum.Enum):
    TEST = "test"
    DEV = "dev"
    PROD = "prod"


class ApiSettings(BaseSettings, ABC):
    API_ENV: str = ApiEnvironment.DEV
    SECRET_KEY: str  # secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    BACKEND_CORS_ORIGINS: list[str] = []
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    TIMEZONE: str = "Chile/Santiago"
    PROJECT_ROOT_DIR: DirectoryPath = Path(__file__).parent.parent

    @property
    def project_name(self) -> str:
        return f"Pinochet - Rettig ({self.API_ENV})"

    @property
    def db_uri(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD.get_secret_value(),
                host=self.POSTGRES_HOST,
                path=self.POSTGRES_DB,
                port=self.POSTGRES_PORT,
            )
        )

    class Config:
        case_sensitive = True


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

    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr = "postgres"
    POSTGRES_DB: str = "pinochet"
    POSTGRES_PORT: int = 5433


class TestSettings(DevSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5434
    POSTGRES_USER: str = "postgres_test"
    POSTGRES_PASSWORD: SecretStr = "postgres_password_test"
    POSTGRES_DB: str = "pinochet_test"


@lru_cache
def get_settings(env: ApiEnvironment = ApiEnvironment.DEV) -> ApiSettings:
    """Dispatch settings based on environment variable API_ENV.

    Defaults to "dev" with a warning if API_ENV is not set.
    """

    # Settings are cached
    return _environment_dispatch[env]


_environment_dispatch: Dict[str, Any] = {
    ApiEnvironment.TEST: TestSettings(),
    ApiEnvironment.DEV: DevSettings(),
    ApiEnvironment.PROD: ProdSettings(),
}
