from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    location_id: Optional[int] = None
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    exact_coordinates: Optional[bool]
    geometry: Optional[str] = None
    srid: str = "4326"


class LocationExtraPlace(Location):
    place: Optional[str]
    location_n: Optional[int]


class LocationOut(Location):
    class Config:
        from_attributes = True
