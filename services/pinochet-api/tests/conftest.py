import logging  # Add this line to import the missing module
import typing
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pinochet import models
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------- #
#                             utilities for testing                            #
# ---------------------------------------------------------------------------- #

# https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/


def teardown_db(session: Session) -> None:
    # drop all tables
    models.Base.metadata.drop_all(bind=session.bind)


def setup_db(session: Session) -> None:
    # create all tables
    models.Base.metadata.create_all(bind=session.bind)


# ---------------------------------------------------------------------------- #
#                                begin fixtures                                #
# ---------------------------------------------------------------------------- #

# Annotation for the session fixture
_Session = typing.TypeVar("_Session", bound="Session")


def get_settings_override():
    from pinochet.settings import TestSettings

    return TestSettings()


def get_db_override():
    from pinochet.db import SessionLocal

    db = SessionLocal()
    return db


@pytest.fixture()
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """

    from pinochet.main import create_app
    from pinochet.settings import get_settings
    from pinochet.api.deps import get_db

    app = create_app()

    # override the get_settings dependency with a test settings object
    # https://fastapi.tiangolo.com/advanced/settings/#settings-and-testing
    app.dependency_overrides[get_settings] = get_settings_override

    # replace the get_db dependency with our own during testing
    app.dependency_overrides[get_db] = get_db_override

    return app


@pytest.fixture()
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def session(app: FastAPI) -> Generator[_Session, Any, None]:
    from pinochet.db import get_db

    session = next(get_db())

    setup_db(session)
    yield session
    session.close()
    teardown_db(session)


@pytest.fixture()
def test_user(session: _Session) -> Generator[models.User, Any, None]:
    from pinochet.api.core.security import get_password_hash

    test_user = models.User(
        email="test@pinochet-analyze-50.cl",
        username="test_user",
        hashed_password=get_password_hash("test_pass"),
    )

    logger.info(f"Adding user {test_user.username} ({test_user.email})")
    session.add(test_user)
    session.commit()

    yield test_user


@pytest.fixture()
def test_token(client: TestClient, test_user: models.User) -> str:
    data = {"username": test_user.username, "password": "test_pass"}
    login_endpoint = client.app.url_path_for("login_for_access_token")
    response = client.post(login_endpoint, data=data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token
