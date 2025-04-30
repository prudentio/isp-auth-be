from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.region_aggregate import RegionAggregates
from app.models.region import Regions
from typing import Optional, List, Dict, TypedDict
from datetime import date

class RegionAggregateSummary(TypedDict):
    id: str
    name: str
    total: int

async def get_region_aggregate_data(
    db: AsyncSession,
    kec_id: Optional[List[str]] = None,
    kel_id: Optional[List[str]] = None,
    rw_id: Optional[List[str]] = None,
    rt_id: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Dict[str, List[RegionAggregateSummary]]:
    filters = []

    if kec_id:
        filters.append(RegionAggregates.kec_id.in_(kec_id))
    if kel_id:
        filters.append(RegionAggregates.kel_id.in_(kel_id))
    if rw_id:
        filters.append(RegionAggregates.rw_id.in_(rw_id))
    if rt_id:
        filters.append(RegionAggregates.rt_id.in_(rt_id))
    if start_date:
        filters.append(RegionAggregates.date >= start_date)
    if end_date:
        filters.append(RegionAggregates.date <= end_date)

    def build_query(region_field: str):
        return (
            select(
                getattr(RegionAggregates, region_field).label("id"),
                Regions.name.label("name"),
                func.sum(RegionAggregates.total_data).label("total"),
            )
            .join(Regions, getattr(RegionAggregates, region_field) == Regions.id)
            .where(and_(*filters) if filters else True)
            .group_by(getattr(RegionAggregates, region_field), Regions.name)
        )

    kecamatan_query = await db.execute(build_query("kec_id"))
    kelurahan_query = await db.execute(build_query("kel_id"))
    rt_query = await db.execute(build_query("rt_id"))

    return {
        "kecamatan": [{"id": row.id, "name": row.name, "total": row.total} for row in kecamatan_query],
        "kelurahan": [{"id": row.id, "name": row.name, "total": row.total} for row in kelurahan_query],
        "rt": [{"id": row.id, "name": row.name, "total": row.total} for row in rt_query],
    }
