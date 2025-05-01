from fastapi import APIRouter, Depends, Query, status
from app.infrastructure.db.session import get_db_dashboard
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.services.surveyor_aggregate import get_aggregated_surveyor_data
from app.schemas.response import SuccessResponse
from app.exceptions import CustomHTTPException

router = APIRouter()

@router.get("", response_model=SuccessResponse)
async def get_surveyor_aggregate(
    db: AsyncSession = Depends(get_db_dashboard),
    rt_id: Optional[List[str]] = Query(None),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
    ):
    
    data = await get_aggregated_surveyor_data(db, rt_id, start_date, end_date)

    if not data:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="there is no data found"
        )
    
    return SuccessResponse(
          status_code=status.HTTP_200_OK,
          data=data
    )