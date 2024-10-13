import datetime as dt
import typing

import strawberry
from pinochet.api.v1.graphql.auth import IsAuthenticated
from pinochet.api.v1.graphql.context import Context
from pinochet import models
from sqlalchemy.orm import Session
from strawberry.extensions import QueryDepthLimiter
from strawberry.types import Info


@strawberry.type
class Location:
    location_id: typing.Optional[int] = None
    location_name: typing.Optional[str] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None
    exact_coordinates: typing.Optional[bool] = None
    geometry: typing.Optional[str] = None
    srid: typing.Optional[str] = None

    # many to many relationship managed by SQLAlchemy
    events_ids: typing.Optional[typing.List[int]] = None

    @classmethod
    def marshal(cls, model: models.Location) -> "Location":
        return cls(
            location_id=strawberry.ID(str(model.location_id)),
            location_name=model.location_name,
            latitude=model.latitude,
            longitude=model.longitude,
            exact_coordinates=model.exact_coordinates,
            geometry=model.geometry,
            srid=model.srid,
            events_ids=(
                [event.event_id for event in model.events] if model.events else None
            ),
        )


@strawberry.type
class Event:
    event_id: typing.Optional[int] = None
    victim_id: typing.Optional[int] = None
    group_id: typing.Optional[int] = None
    start_date_daily: typing.Optional[dt.datetime] = None
    end_date_daily: typing.Optional[dt.datetime] = None
    violence: typing.Optional[str] = None
    method: typing.Optional[str] = None
    interrogation: typing.Optional[bool] = None
    torture: typing.Optional[bool] = None
    mistreatment: typing.Optional[bool] = None
    targeted: typing.Optional[str] = None
    press: typing.Optional[bool] = None
    war_tribunal: typing.Optional[bool] = None
    number_previous_arrests: typing.Optional[int] = None
    perpetrator_affiliation: typing.Optional[str] = None
    perpetrator_affiliation_detail: typing.Optional[str] = None
    page: typing.Optional[str] = None

    # many to many relationship managed by SQLAlchemy
    locations_ids: typing.Optional[typing.List[int]] = None

    @classmethod
    def marshal(cls, model: models.Event) -> "Event":
        return cls(
            event_id=strawberry.ID(str(model.event_id)),
            victim_id=strawberry.ID(str(model.victim_id)),
            group_id=strawberry.ID(str(model.group_id)),
            start_date_daily=model.start_date_daily,
            end_date_daily=model.end_date_daily,
            violence=model.violence,
            method=model.method,
            interrogation=model.interrogation,
            torture=model.torture,
            mistreatment=model.mistreatment,
            targeted=model.targeted,
            press=model.press,
            war_tribunal=model.war_tribunal,
            number_previous_arrests=model.number_previous_arrests,
            perpetrator_affiliation=model.perpetrator_affiliation,
            perpetrator_affiliation_detail=model.perpetrator_affiliation_detail,
            page=model.page,
            locations_ids=(
                [location.location_id for location in model.locations]
                if model.locations
                else None
            ),
        )


@strawberry.type
class Victim:
    victim_id: typing.Optional[int] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    minor: typing.Optional[bool] = None
    age: typing.Optional[float] = None
    male: typing.Optional[bool] = None
    occupation: typing.Optional[str] = None
    occupation_detail: typing.Optional[str] = None
    victim_affiliation: typing.Optional[str] = None
    victim_affiliation_detail: typing.Optional[str] = None
    nationality: typing.Optional[str] = None

    # one to many relationship managed by SQLAlchemy
    events_ids: typing.Optional[typing.List[int]] = None

    @classmethod
    def marshal(cls, model: models.Victim) -> "Victim":
        return cls(
            victim_id=strawberry.ID(str(model.victim_id)),
            first_name=model.first_name,
            last_name=model.last_name,
            minor=model.minor,
            age=model.age,
            male=model.male,
            occupation=model.occupation,
            occupation_detail=model.occupation_detail,
            victim_affiliation=model.victim_affiliation,
            victim_affiliation_detail=model.victim_affiliation_detail,
            nationality=model.nationality,
            events_ids=(
                [event.event_id for event in model.events] if model.events else None
            ),
        )


def get_victims(session: Session) -> typing.List[Victim]:
    with session.begin():
        victims = session.query(models.Victim).order_by(models.Victim.victim_id).all()

    return [Victim.marshal(victim) for victim in victims]


def get_events(session: Session) -> typing.List[Event]:
    with session.begin():
        events = session.query(models.Event).order_by(models.Event.event_id).all()
    return [Event.marshal(event) for event in events]


def get_locations(session: Session) -> typing.List[Location]:
    with session.begin():
        locations = (
            session.query(models.Location).order_by(models.Location.location_id).all()
        )
    return [Location.marshal(location) for location in locations]


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def victims(self, info: Info) -> typing.List[Victim]:
        context: Context = info.context
        db = context.db
        return get_victims(session=db)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def events(self, info: Info) -> typing.List[Event]:
        context: Context = info.context
        db = context.db
        return get_events(session=db)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def locations(self, info: Info) -> typing.List[Location]:
        context: Context = info.context
        db = context.db
        return get_locations(session=db)


schema = strawberry.Schema(
    query=Query,
    extensions=[QueryDepthLimiter(max_depth=3)],
)
