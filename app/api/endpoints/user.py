from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.middleware.jwt_auth import get_current_user
from app.schemas.response import SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import CustomHTTPException
from app.schemas.user import UserInfoResponse
from app.infrastructure.db.session import get_db_dashboard
from app.services.user import get_user_regions_by_user_id

router = APIRouter()

@router.get("", response_model=SuccessResponse[UserInfoResponse])
async def get_user_info(
    user_id: Annotated[str, Depends(get_current_user)], 
    db: AsyncSession = Depends(get_db_dashboard)
):
    user_region_ids = await get_user_regions_by_user_id(db, user_id)

    if not user_region_ids:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="there is no region id found"
        )

    return SuccessResponse(
          status_code=status.HTTP_200_OK,
          data=UserInfoResponse(
              user_id=user_id,
              region_ids=user_region_ids
          )
    )