from fastapi import FastAPI
from fastapi.testclient import TestClient
from pinochet import models, schemas
from sqlalchemy.orm import Session
import pytest
from sqlalchemy_model_faker import factory


def test_get_all_events(
    app: FastAPI,
    client: TestClient,
    session: Session,
    test_token: str,
) -> None:
    N_EVENTS = 5

    # create fake events
    fake_events = [
        factory(models.Event).make(
            ignored_columns=["locations"],
        )
        for _ in range(N_EVENTS)
    ]

    # for each event, create 1 fake victim
    for event in fake_events:
        event.victim = factory(models.Victim).make(
            ignored_columns=["events"],
        )

    session.add_all(fake_events)
    session.commit()

    # get events from session back
    events_in_db = session.query(models.Event).all()

    # convert instances to schemas
    events_in = [schemas.EventOut.model_validate(c) for c in fake_events]

    # construct headers
    headers = {"Authorization": f"Bearer {test_token}"}

    # construct params
    params = {"limit": len(events_in_db)}
    assert len(events_in_db) == N_EVENTS

    # check that the api returns all of the instances in the database
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
