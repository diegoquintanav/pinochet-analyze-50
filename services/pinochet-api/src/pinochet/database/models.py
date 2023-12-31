import datetime as dt
import typing

from pinochet.database.base import Base
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

event_location_association = Table(
    "api_pinochet__event_location_association",
    Base.metadata,
    Column(
        "event_id",
        Integer,
        ForeignKey("api.api_pinochet__event.event_id"),
        primary_key=True,
    ),
    Column(
        "location_id",
        Integer,
        ForeignKey("api.api_pinochet__location.location_id"),
        primary_key=True,
    ),
    schema="api",
)


class Victim(Base):
    __tablename__ = "api_pinochet__victim"
    __table_args__ = {"schema": "api"}

    victim_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    minor: Mapped[bool] = mapped_column(Boolean)
    age: Mapped[int] = mapped_column(Integer)
    male: Mapped[bool] = mapped_column(Boolean)
    occupation: Mapped[str] = mapped_column(String)
    occupation_detail: Mapped[str] = mapped_column(String)
    victim_affiliation: Mapped[str] = mapped_column(String)
    victim_affiliation_detail: Mapped[str] = mapped_column(String)
    nationality: Mapped[str] = mapped_column(String)

    # Victim -|-* Events
    events: Mapped[typing.List["Event"]] = relationship(
        "Event",
        lazy="joined",
        back_populates="victim",
    )


class Location(Base):
    __tablename__ = "api_pinochet__location"
    __table_args__ = {"schema": "api"}

    location_id: Mapped[int] = mapped_column(primary_key=True)
    location_name: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)
    exact_coordinates: Mapped[bool] = mapped_column(Boolean)
    geometry: Mapped[str] = mapped_column(String)
    srid: Mapped[str] = mapped_column(String)

    events: Mapped[typing.List["Event"]] = relationship(
        secondary=event_location_association,
        back_populates="locations",
        lazy="joined",
    )


class Event(Base):
    __tablename__ = "api_pinochet__event"
    __table_args__ = {"schema": "api"}

    event_id: Mapped[int] = mapped_column(primary_key=True)
    victim_id: Mapped[int] = mapped_column(
        ForeignKey("api.api_pinochet__victim.victim_id")
    )
    group_id: Mapped[int] = mapped_column(Integer)
    start_date_daily: Mapped[dt.date] = mapped_column(Date)
    end_date_daily: Mapped[dt.date] = mapped_column(Date)
    violence: Mapped[str] = mapped_column(String)
    method: Mapped[str] = mapped_column(String)
    interrogation: Mapped[bool] = mapped_column(Boolean)
    torture: Mapped[bool] = mapped_column(Boolean)
    mistreatment: Mapped[bool] = mapped_column(Boolean)
    targeted: Mapped[str] = mapped_column(String)
    press: Mapped[bool] = mapped_column(Boolean)
    war_tribunal: Mapped[bool] = mapped_column(Boolean)
    number_previous_arrests: Mapped[int] = mapped_column(Integer)
    perpetrator_affiliation: Mapped[str] = mapped_column(String)
    perpetrator_affiliation_detail: Mapped[str] = mapped_column(String)
    page: Mapped[str] = mapped_column(String)

    victim: Mapped["Victim"] = relationship(
        "Victim",
        lazy="joined",
        back_populates="events",
    )

    # assumed that an event has only one victim,
    locations: Mapped[typing.List["Location"]] = relationship(
        "Location",
        secondary=event_location_association,
        back_populates="events",
        lazy="joined",
    )


if __name__ == "__main__":
    from pinochet.database.session import SessionLocal

    sess = SessionLocal()

    sess.query(Event).all()

    e = sess.query(Event).first()

    print(e.event_id)

    print(e.victim_id)

    _location = sess.query(Location).first()
