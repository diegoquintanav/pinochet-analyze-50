from fastapi import FastAPI
from fastapi.testclient import TestClient
from pinochet import models, schemas
from sqlalchemy.orm import Session

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


def test_get_events_around_self(
    app: FastAPI,
    client: TestClient,
    db: Session,
    test_token: str,
) -> None:
    # Assuming one event has one victim only
    # Many events may have the same location

    victims = []  # noqa
    locations = []  # noqa
    events = []  # noqa

    for i in range(1, 4):
        victim = models.Victim(
            # victim_id=i + 1000,
            first_name=f"test-{i}",
            last_name=f"victim-{i}",
            age=i,
        )

        db.add(victim)
        db.commit()

        # location = models.Location(
        #     location_name=f"test-location-{i}",
        #     latitude=0,
        #     longitude=0,
        # )

        # event = models.Event(
        #     victim=victim,
        #     locations=[location],)

        # victims.append(victim)
        # locations.append(location)
        # events.append(event)

    # db.add_all([*victims, *locations, *events])
    # db.commit()
    # db.flush()

    # update n-1 events to have the a location within 10 km of the first event

    # get the first event

    # call the api with the first event_id and a radius of 10

    # check that the response contains the n-1 events
