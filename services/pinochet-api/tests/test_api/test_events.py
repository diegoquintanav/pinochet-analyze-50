from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pinochet.database import models
from pinochet import schemas


def test_get_all_events(
    app: FastAPI,
    client: TestClient,
    db: Session,
    test_token: str,
) -> None:
    events = db.query(models.Event).all()
    assert len(events) > 0

    # convert biomass_fuel to schemas
    events_in = [schemas.EventOut.model_validate(c) for c in events]

    # construct headers
    headers = {"Authorization": f"Bearer {test_token}"}

    # construct params
    params = {"limit": len(events)}

    # check that the api returns all of the biomass_fuel in the database
    r = client.get(
        app.url_path_for("get_multi_events"),
        params=params,
        headers=headers,
    )

    response = r.json()

    assert len(response) == len(events_in)

    # sort by id and compare them individually
    response = sorted(response, key=lambda x: x["event_id"])
    response_sorted = sorted(response, key=lambda x: x["event_id"])

    for x, y in zip(response_sorted, response, strict=True):
        assert x == y
