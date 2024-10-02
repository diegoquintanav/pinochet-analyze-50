import datetime as dt
import logging
import typing

from pinochet.base import Base
from pinochet.time import utcnow
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

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

    def get_events_around_self(
        self,
        session,
        *,
        radius: int,
    ) -> typing.List["Event"]:
        """
        Get all events around a given event id within a certain radius.
        """
        # http://postgis.net/docs/manual-1.3/ch03.html#id434832

        schema = self.__table_args__["schema"]
        table = self.__tablename__

        subquery = f"""
        SELECT geometry
        FROM {schema}.{table}
        WHERE event_id = :event_id
        """

        query = f"""
        SELECT *
        FROM {schema}.{table}
        WHERE ST_DWithin(
            geometry,
            ({subquery}), :radius)
        """

        logger.debug(f"Query: {query}")

        return session.execute(
            text(query), {"event_id": self.event_id, "radius": radius}
        ).fetchall()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "api"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)  # fmt: skip
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=utcnow())  # fmt: skip
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=utcnow())  # fmt: skip
    last_seen_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), onupdate=utcnow(), nullable=True)  # fmt: skip


# class Token(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


if __name__ == "__main__":
    from pinochet.db import SessionLocal

    sess = SessionLocal()

    sess.query(Event).all()

    e = sess.query(Event).first()

    print(e.event_id)

    print(e.victim_id)

    _location = sess.query(Location).first()
