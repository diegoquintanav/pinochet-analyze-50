from typing import Optional

from pydantic import BaseModel


class Victim(BaseModel):
    individual_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    minor: Optional[bool] = None
    age: Optional[float] = None
    male: Optional[bool] = None
    occupation: Optional[str] = None
    occupation_detail: Optional[str] = None
    victim_affiliation: Optional[str] = None
    victim_affiliation_detail: Optional[str] = None
    nationality: Optional[str] = None


class VictimOut(Victim):
    class Config:
        from_attributes = True
