from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pinochet import models
from pinochet import schemas
from sqlalchemy_model_faker import factory


def test_get_all_victims(
    app: FastAPI,
    client: TestClient,
    session: Session,
    test_token: str,
) -> None:
    N_VICTIMS = 5

    fake_victims = [
        factory(models.Victim).make(
            ignored_columns=["events"],
        )
        for _ in range(N_VICTIMS)
    ]

    session.add_all(fake_victims)
    session.commit()

    victims_in_db = session.query(models.Victim).all()
    assert len(victims_in_db) == N_VICTIMS

    # convert biomass_fuel to schemas
    victims_in = [schemas.VictimOut.model_validate(c) for c in victims_in_db]

    # construct headers
    headers = {"Authorization": f"Bearer {test_token}"}

    # construct params
    params = {"limit": len(victims_in_db)}

    # check that the api returns all of the biomass_fuel in the database
    r = client.get(
        app.url_path_for("get_multi_victims"),
        params=params,
        headers=headers,
    )

    response = r.json()

    assert len(response) == len(victims_in)

    # sort by id and compare them individually
    response = sorted(response, key=lambda x: x["victim_id"])
    response_sorted = sorted(response, key=lambda x: x["victim_id"])

    for x, y in zip(response_sorted, response, strict=True):
        assert x == y
