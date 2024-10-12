from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "Healthy"


def test_env_is_testing(app) -> None:
    assert app.title == "Pinochet - Rettig (test)"


def test_db_is_testing(session: Session) -> None:
    assert session.bind.engine.url.database == "pinochet_test"
