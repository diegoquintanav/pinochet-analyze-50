import datetime as dt
import logging
import typing

from geoalchemy2 import Geometry, WKBElement
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
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text

from pinochet.base import Base
from pinochet.time import utcnow

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
    geometry: Mapped[WKBElement] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            spatial_index=True,
        )
    )
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
        session: Session,
        *,
        radius: int,
        limit: int = 10,
    ) -> typing.List["Event"]:
        """
        Get all events around a given event id within a certain radius.
        """
        # http://postgis.net/docs/manual-1.3/ch03.html#id434832

        schema = self.__table_args__["schema"]
        table = self.__tablename__

        session.execute(text(f"SET search_path TO {schema}"))

        # https://medium.com/@notarious2/working-with-spatial-data-using-fastapi-and-geoalchemy-797d414d2fe7
        # https://docs.sqlalchemy.org/en/20/_modules/examples/postgis/postgis.html

        query = text(
            """
        WITH denormalized_location_events AS (
          SELECT
            ape.event_id,
            apela.location_id,
            apl.geometry,
            apl.location_name
          FROM
            api_pinochet__event AS ape
          LEFT JOIN api_pinochet__event_location_association AS apela ON
            ape.event_id = apela.event_id
          LEFT JOIN api_pinochet__location AS apl ON
            apela.location_id = apl.location_id
        ),

        observed_event AS (
          SELECT
            *
          FROM
            denormalized_location_events
          WHERE
            event_id = :event_id
        ),

        other_events AS (
          SELECT
            *
          FROM
            denormalized_location_events
          WHERE
            event_id != :event_id
        )

        -- final query
        SELECT
          -- ST_Distance(d1.geometry::geography, d2.geometry::geography) AS d1d2_dist,
          d1.event_id as d1_event_id,
          d1.location_id as d1_location_id,
          d1.geometry as d1_geometry,
          d1.location_name as d1_location_name,
          d2.event_id as d2_event_id,
          d2.location_id as d2_location_id,
          d2.geometry as d2_geometry,
          d2.location_name as d2_location_name
        FROM
          observed_event AS d1,
          other_events AS d2
        WHERE
          ST_DWithin(
            d2.geometry,
            (
              SELECT
                geometry
              FROM
                observed_event
            ),
            :radius -- in meters
          )
        ORDER BY d1d2_dist ASC -- closest first
        LIMIT :limit -- limit the number of results
        """
        )

        logger.debug(f"Query: {query}")

        return session.execute(
            query,
            {
                "event_id": self.event_id,
                "radius": radius,
                "limit": limit,
            },
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
    from pinochet.db import get_db

    sess = next(get_db())

    sess.query(Event).all()

    e = sess.query(Event).first()

    print(e.event_id)

    print(e.victim_id)

    _location = sess.query(Location).first()
