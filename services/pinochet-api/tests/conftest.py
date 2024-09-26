import logging  # Add this line to import the missing module
import typing
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pinochet.api.core.security import get_password_hash
from pinochet.api.deps import get_db
from pinochet.database.models import User
from pinochet.main import create_app
from sqlalchemy.orm import Session

#
logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------- #
#                             utilities for testing                            #
# ---------------------------------------------------------------------------- #

# https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/


def teardown_db(session: Session) -> None:
    logger.warning("Database setup managed by dbt. Not doing anything here.")


def setup_db(session: Session) -> None:
    logger.warning("Database setup managed by dbt. Not doing anything here.")


# ---------------------------------------------------------------------------- #
#                                begin fixtures                                #
# ---------------------------------------------------------------------------- #


_S = typing.TypeVar("_S", bound="Session")


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """

    app = create_app(title="Test app")

    return app


@pytest.fixture(scope="session")
def session(app: FastAPI) -> Generator[_S, Any, None]:
    from pinochet.database.session import SessionLocal as SessionTesting

    yield SessionTesting()


@pytest.fixture(scope="session")
def db(session: Session, app: FastAPI) -> Generator[_S, Any, None]:
    setup_db(session)
    yield session
    session.close()
    teardown_db(session)


@pytest.fixture(scope="function")
def client(app: FastAPI, db: _S) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        yield db

    # replace the get_db dependency with our own during testing
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as client:
        yield client


@pytest.fixture()
def test_user(db: Session) -> User:
    test_user = User(
        email="test@pinochet-analyze-50.cl",
        username="test_user",
        hashed_password=get_password_hash("test_pass"),
    )

    logger.info(f"Deleting {test_user.username} from database, if exists")
    db.query(User).filter(User.username == test_user.username).delete()

    logger.info(f"Adding user {test_user.username} ({test_user.email})")
    db.add(test_user)
    db.commit()

    return test_user


@pytest.fixture()
def test_token(client: TestClient, test_user: User) -> str:
    data = {"username": test_user.username, "password": "test_pass"}
    login_endpoint = client.app.url_path_for("login_for_access_token")
    response = client.post(login_endpoint, data=data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token
