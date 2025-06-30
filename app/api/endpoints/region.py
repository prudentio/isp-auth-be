from fastapi import APIRouter, Depends, status,  Query
from app.middleware.jwt_auth import get_current_user
from app.schemas.response import SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import CustomHTTPException
from app.infrastructure.db.session import get_db_dashboard
from app.schemas.region import GetRegionByLevelResponse, RegionLevel
from app.services.region import get_region_by_level
from typing import Annotated, List

router = APIRouter()

@router.get("",response_model=SuccessResponse[List[GetRegionByLevelResponse]])
async def read_regions_by_level(
    user_id: Annotated[str, Depends(get_current_user)], 
    level: Annotated[RegionLevel, Query(...)],
    db: AsyncSession = Depends(get_db_dashboard)
):
    data = await get_region_by_level(db, level.name)

    if not data:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="there is no region found"
        )
    
    return SuccessResponse(
          status_code=status.HTTP_200_OK,
          data=data
    )