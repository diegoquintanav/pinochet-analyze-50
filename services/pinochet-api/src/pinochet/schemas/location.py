import datetime as dt
import uuid
from random import choice
from typing import List, Optional, Union
from uuid import uuid4

from pydantic import UUID3, UUID4, BaseModel, EmailStr, Field


class Location(BaseModel):
    location_id: Optional[int] = None
    place: Optional[str]
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    exact_coordinates: Optional[bool]
    location_n: Optional[int]
    geometry: Optional[str] = None
    srid: str = "4326"


class LocationOut(Location):
    class Config:
        from_attributes = True
