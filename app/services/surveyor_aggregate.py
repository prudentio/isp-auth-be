from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, func, and_
from typing import Optional, List, Dict, TypedDict, NotRequired
from datetime import date
from app.models.surveyor_aggregate import SurveyorAggregates
from app.schemas.surveyor_aggregate import SurveyorAggregateResponseData

class SurveyorAggregateSummary(TypedDict):
    surveyor_name: str
    surveyor_id: str
    total_data: int
    date: NotRequired[date]

def append_region_filter(
    filters: List, 
    region_type:str, 
    region: Optional[List]
) -> List:
    if region is None:
        return filters
    
    if region_type == 'rt_id':
        filters.append(SurveyorAggregates.rt_id.in_(region))
        return filters
    
    like_filters = [SurveyorAggregates.rt_id.ilike(f"%{r}%") for r in region]
    filters.append(or_(*like_filters))

    return filters

def build_query(is_for_export_excel: bool, filters: List):
    select_cols = [
        SurveyorAggregates.surveyor_name,
        SurveyorAggregates.surveyor_id,
        func.sum(SurveyorAggregates.total_data).label("total_data")
    ]

    group_by_cols = [SurveyorAggregates.surveyor_id]

    if is_for_export_excel:
        select_cols.insert(0, SurveyorAggregates.date)
        group_by_cols.insert(0, SurveyorAggregates.date)
    
    query = select(*select_cols)

    query = query.where(and_(*filters)) if filters else query

    query = query.group_by(*group_by_cols)

    return query

async def get_aggregated_surveyor_data(
    db: AsyncSession,
    kec_id: Optional[List[str]] = None,
    kel_id: Optional[List[str]] = None,
    rw_id: Optional[List[str]] = None,
    rt_id: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_for_export_excel: Optional[bool] = False
) -> Dict[str, List[SurveyorAggregateSummary]]:
    filters = []

    filters = append_region_filter(filters, "kec_id", kec_id)
    filters = append_region_filter(filters, "kel_id", kel_id)
    filters = append_region_filter(filters,"rw_id", rw_id)
    filters = append_region_filter(filters,"rt_id", rt_id)

    if start_date:
        filters.append(SurveyorAggregates.date >= start_date)
    if end_date:
        filters.append(SurveyorAggregates.date <= end_date)
   

    query = build_query(is_for_export_excel, filters)

    result = await db.execute(query)

    rows = result.fetchall()

    summary = [
        (SurveyorAggregateResponseData(
            date=row.date if is_for_export_excel else None,
            surveyor_name = row.surveyor_name,
            surveyor_id = row.surveyor_id,
            total_data=row.total_data
        ))  for row in rows
    ]

    return summary