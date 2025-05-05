from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.region_aggregate import RegionAggregates
from app.models.region import Regions
from typing import Optional, List, Dict, TypedDict, NotRequired
from datetime import date

class RegionAggregateSummary(TypedDict):
    id: str
    name: str
    total: int
    date: NotRequired[date]

def build_query(
    region_field: str, 
    is_for_export_excel: bool, 
    filters: List
):
    region_col = getattr(RegionAggregates, region_field)

    select_cols = [
        region_col.label("id"),
        Regions.name,
        func.sum(RegionAggregates.total_data).label("total"),
    ]

    group_by_cols = [region_col]

    if is_for_export_excel:
        select_cols.insert(0, RegionAggregates.date)
        group_by_cols.insert(0, RegionAggregates.date)
    
    query = select(*select_cols).join(Regions, region_col == Regions.id)

    if filters:
        query = query.where(and_(*filters))

    query = query.group_by(*group_by_cols)

    return query


async def fetch_and_format(
    db: AsyncSession, 
    region_field: str, 
    is_for_export_excel: bool, 
    filters: List
):
    result = await db.execute(build_query(region_field, is_for_export_excel, filters))
    rows = result.fetchall()

    return [
        {
            **({"date": row.date} if is_for_export_excel else {}),
            "id": row.id,
            "name": row.name,
            "total": row.total,
        }
        for row in rows
    ]


def append_region_filter(
    filters: List, 
    region_type: str, 
    region: Optional[List]
) -> List:
    if region is None:
        return filters

    filters.append(getattr(RegionAggregates, region_type).in_(region))
    return filters

async def get_aggregated_region_data(
    db: AsyncSession,
    kec_id: Optional[List[str]] = None,
    kel_id: Optional[List[str]] = None,
    rw_id: Optional[List[str]] = None,
    rt_id: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_for_export_excel: Optional[bool] = False
) -> Dict[str, List[RegionAggregateSummary]]:
    filters = []

    filters = append_region_filter(filters, "kec_id", kec_id)
    filters = append_region_filter(filters, "kel_id", kel_id)
    filters = append_region_filter(filters,"rw_id", rw_id)
    filters = append_region_filter(filters,"rt_id", rt_id)
    
    if start_date:
        filters.append(RegionAggregates.date >= start_date)
    if end_date:
        filters.append(RegionAggregates.date <= end_date)

    return {
        "kecamatan": await fetch_and_format(db, "kec_id", is_for_export_excel, filters),
        "kelurahan": await fetch_and_format(db, "kel_id", is_for_export_excel, filters),
        "rt": await fetch_and_format(db, "rt_id", is_for_export_excel, filters),
    }
