from fastapi import APIRouter, Depends, Query, status
from app.infrastructure.db.session import get_db_dashboard
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from datetime import date
from app.middleware.jwt_auth import get_current_user
from app.services.region_aggregate import get_aggregated_region_data
from app.schemas.response import SuccessResponse
from app.exceptions import CustomHTTPException

router = APIRouter()

@router.get("", response_model=SuccessResponse)
async def get_region_aggregate(
    user_id: Annotated[str, Depends(get_current_user)], 
    db: AsyncSession = Depends(get_db_dashboard),
    kec_id: Annotated[List[str] | None, Query()] = None,
    kel_id: Annotated[List[str] | None, Query()] = None,
    rw_id: Annotated[List[str] | None, Query()] = None,
    rt_id: Annotated[List[str] | None, Query()] = None,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None
):
    data = await get_aggregated_region_data(
        db=db,
        kec_id=kec_id,
        kel_id=kel_id,
        rw_id=rw_id,
        rt_id=rt_id,
        start_date=start_date,
        end_date=end_date
    )

    if not data:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="there is no data found"
        )
    
    return SuccessResponse(
          status_code=status.HTTP_200_OK,
          data=data
    )