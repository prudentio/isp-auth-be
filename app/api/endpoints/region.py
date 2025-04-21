from fastapi import APIRouter, Depends, status,  Query
from app.schemas.response import SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import CustomHTTPException
from app.infrastructure.db.session import get_db
from app.schemas.region import GetRegionByLevelResponse, RegionLevel
from app.services.region import get_region_by_level
from typing import List

router = APIRouter()

@router.get("",response_model=SuccessResponse[List[GetRegionByLevelResponse]])
async def read_regions_by_level(level: RegionLevel = Query(...), db: AsyncSession = Depends(get_db)):
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