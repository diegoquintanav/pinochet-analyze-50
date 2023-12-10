import datetime as dt

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
from sqlalchemy.orm import Mapped, mapped_column

event_location_association = Table(
    "event_location",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("event.event_id")),
    Column("location_id", Integer, ForeignKey("location.location_id")),
)


class Victim(Base):
    __tablename__ = "api_pinochet__victim"
    __table_args__ = {"schema": "api"}

    individual_id: Mapped[int] = mapped_column(primary_key=True)
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


class Location(Base):
    __tablename__ = "api_pinochet__location"
    __table_args__ = {"schema": "api"}

    location_id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)
    exact_coordinates: Mapped[bool] = mapped_column(Boolean)
    geometry: Mapped[str] = mapped_column(String)
    srid: Mapped[str] = "4326"


class Event(Base):
    __tablename__ = "api_pinochet__event"
    __table_args__ = {"schema": "api"}

    event_id: Mapped[int] = mapped_column(primary_key=True)
    individual_id: Mapped[int] = mapped_column(Integer)
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
