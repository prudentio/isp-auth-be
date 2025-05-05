from typing import Optional
from app.schemas.response import CamelModel
from datetime import date

class SurveyorAggregateResponseData(CamelModel):
    date: Optional[date]
    surveyor_id: str
    surveyor_name: str
    total_data: int