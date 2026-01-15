from pydantic import BaseModel, Field, conint
from typing import List, Optional


class ItineraryRequest(BaseModel):
    from_city: Optional[str] = None
    destination: str = Field(..., example="hampi")
    days: conint(ge=1, le=5)
    pace: str = Field(..., example="balanced")
    interests: List[str] = []
    arrival_time: Optional[str] = "08:00"


class TimeSlot(BaseModel):
    morning: List[str] = []
    afternoon: List[str] = []
    evening: List[str] = []


class DayPlan(BaseModel):
    day: int
    schedule: TimeSlot
    food: List[str] = []
    stay_area: Optional[str] = None
    commute_tips: Optional[str] = None


class ItineraryResponse(BaseModel):
    destination: str
    days: List[DayPlan]
