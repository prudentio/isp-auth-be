from app.schemas.response import CamelModel

class SurveyorAggregateResponseData(CamelModel):
    surveyor_name: str
    surveyor_id: str
    rt_id: str
    total_data: int