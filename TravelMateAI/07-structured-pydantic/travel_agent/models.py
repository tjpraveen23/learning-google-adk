from pydantic import BaseModel
from typing import List

class TravelPlan(BaseModel):
    destination: str
    days: int
    budget: int
    hotel: str
    activities: List[str]