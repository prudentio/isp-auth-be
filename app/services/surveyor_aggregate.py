from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, func, and_
from typing import Optional, List, Dict, TypedDict
from datetime import date
from app.models.surveyor_aggregate import SurveyorAggregates
from app.schemas.surveyor_aggregate import SurveyorAggregateResponseData

class SurveyorAggregateSummary(TypedDict):
    id: int
    surveyor_name: str
    surveyor_id: str
    rt_id: str
    total_data: int

async def get_aggregated_surveyor_data(
    db: AsyncSession,
    rt_id: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Dict[str, List[SurveyorAggregateSummary]]:
    filters = []

    if rt_id:
        like_filters = [SurveyorAggregates.rt_id.ilike(f"%{r}%") for r in rt_id]
        filters.append(or_(*like_filters))
    if start_date:
        filters.append(SurveyorAggregates.date >= start_date)
    if end_date:
        filters.append(SurveyorAggregates.date <= end_date)

    query = select(
        SurveyorAggregates.surveyor_name,
        SurveyorAggregates.surveyor_id,
        SurveyorAggregates.rt_id,
        func.sum(SurveyorAggregates.total_data).label("total_data")
    ).group_by(SurveyorAggregates.surveyor_id)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)

    rows = result.fetchall()

    summary = [
        (SurveyorAggregateResponseData(
        surveyor_name = row.surveyor_name,
        surveyor_id = row.surveyor_id,
        rt_id=row.rt_id,
        total_data=row.total_data
        ))  for row in rows
    ]

    return summary