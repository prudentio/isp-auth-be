from fastapi import APIRouter, Depends, status, Request
from app.schemas.response import SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import CustomHTTPException
from app.schemas.user import UserInfoResponse
from app.infrastructure.db.session import get_db
from app.services.user import get_user_regions_by_user_id

router = APIRouter()

@router.get("", response_model=SuccessResponse[UserInfoResponse])
async def get_user_info(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id

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