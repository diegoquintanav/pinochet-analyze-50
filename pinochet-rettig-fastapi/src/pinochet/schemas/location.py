from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    location_id: Optional[int] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    exact_coordinates: Optional[bool] = None
    geometry: Optional[str] = None
    srid: Optional[int] = None


class LocationExtraPlace(Location):
    place: Optional[str]
    location_n: Optional[int]


class LocationOut(Location):
    class Config:
        from_attributes = True
