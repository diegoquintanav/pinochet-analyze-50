from fastapi import FastAPI
from fastapi.testclient import TestClient
from pinochet import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy_model_faker import factory


def test_get_all_locations(
    app: FastAPI,
    client: TestClient,
    session: Session,
    test_token: str,
) -> None:
    N_LOCATIONS = 5

    fake_locations = [
        factory(models.Location).make(
            ignored_columns=["events"],
        )
        for _ in range(N_LOCATIONS)
    ]

    session.add_all(fake_locations)
    session.commit()

    # get instances from session back
    locations_in_db = session.query(models.Location).all()

    # convert instances to schemas
    locations_in = [schemas.LocationOut.model_validate(c) for c in locations_in_db]

    # construct headers
    headers = {"Authorization": f"Bearer {test_token}"}

    # construct params
    params = {"limit": len(locations_in_db)}
    assert len(locations_in_db) == N_LOCATIONS

    # check that the api returns all of the instances in the database
    r = client.get(
        app.url_path_for("get_multi_locations"),
        params=params,
        headers=headers,
    )

    response = r.json()

    assert len(response) == len(locations_in)

    # sort by id and compare them individually
    response = sorted(response, key=lambda x: x["location_id"])
    response_sorted = sorted(response, key=lambda x: x["location_id"])

    for x, y in zip(response_sorted, response, strict=True):
        assert x == y
