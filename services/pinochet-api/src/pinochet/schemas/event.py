import datetime as dt
from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    event_id: Optional[int] = None
    victim_id: Optional[int] = None
    group_id: Optional[int] = None
    start_date_daily: Optional[dt.datetime] = None
    end_date_daily: Optional[dt.datetime] = None
    start_date_monthly: Optional[dt.datetime] = None
    end_date_monthly: Optional[dt.datetime] = None
    violence: Optional[str] = None
    method: Optional[str] = None
    interrogation: Optional[bool] = None
    torture: Optional[bool] = None
    mistreatment: Optional[bool] = None
    targeted: Optional[str] = None
    press: Optional[bool] = None
    war_tribunal: Optional[bool] = None
    number_previous_arrests: Optional[int] = None
    perpetrator_affiliation: Optional[str] = None
    perpetrator_affiliation_detail: Optional[str] = None
    page: Optional[str] = None


class EventOut(Event):
    class Config:
        from_attributes = True
