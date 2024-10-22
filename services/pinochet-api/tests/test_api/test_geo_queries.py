from fastapi import FastAPI
from fastapi.testclient import TestClient
from pinochet import models, schemas
from sqlalchemy.orm import Session
import pytest
from sqlalchemy_model_faker import factory


def test_get_events_around_self(
    app: FastAPI,
    client: TestClient,
    session: Session,
    test_token: str,
) -> None:
    """Given an event, find all events within a certain radius of the event."""

    N_EVENTS = 3
    N_LOCATIONS = 4

    # define some locations
    londres_38 = [-33.444104539948555, -70.64819710355839]
    estadio_nacional = [-33.466104574139294, -70.61124452140739]
    riggs_nowhere = [40.081742597966844, -86.32614615987228]

    # create fake events
    fake_events: list[models.Event] = [
        factory(models.Event).make(
            {"group_id": ix},
            ignored_columns=["locations"],
        )
        for ix in range(N_EVENTS)
    ]

    # for each event, allocate a victim and N locations with fixed locations
    for ix, event in enumerate(fake_events):
        event.victim = factory(models.Victim).make(
            {"victim_id": ix},
            ignored_columns=["events"],
        )

        if ix == 0:
            _lat, _lon = londres_38
        elif ix == 1:
            _lat, _lon = estadio_nacional
        else:
            _lat, _lon = riggs_nowhere
        event.locations = [
            factory(models.Location).make(
                {
                    "latitude": _lat,
                    "longitude": _lon,
                    "location_name": f"location_{ix}",
                },
                ignored_columns=["events"],
            )
            for _ in range(N_LOCATIONS)
        ]

    session.add_all(fake_events)
    session.commit()

    # query data back
    events_in_db = session.query(models.Event).all()
    locations_in_db = session.query(models.Location).all()
    victims_in_db = session.query(models.Victim).all()

    assert len(events_in_db) == N_EVENTS
    assert len(locations_in_db) == N_EVENTS * N_LOCATIONS
    assert len(victims_in_db) == N_EVENTS

    # convert instances to schemas
    events_in = [schemas.EventOut.model_validate(c) for c in events_in_db]
    locations_in = [schemas.LocationOut.model_validate(c) for c in locations_in_db]
    victims_in = [schemas.VictimOut.model_validate(c) for c in victims_in_db]

    # construct headers
    headers = {"Authorization": f"Bearer {test_token}"}

    params = {"radius_km": 10}

    # get the first event
    r = client.get(
        app.url_path_for(
            "get_events_by_event_id_and_radius",
            event_id=events_in[0].event_id,
        ),
        params=params,
        headers=headers,
    )

    r.raise_for_status()
    response = r.json()

    # since locations close to the first event are the first
    # location for the rest of events, the resulting close events
    # should be all minus self
    expected_locations = N_EVENTS - 1

    assert len(response) == expected_locations

    # call the api with the first event_id and a radius of 10

    # check that the response contains the n-1 events
