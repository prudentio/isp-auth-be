from fastapi import APIRouter, Depends, status
from app.schemas.auth import LoginRequest, LoginResponseData
from app.schemas.response import SuccessResponse
from app.infrastructure.db.session import get_db_dashboard
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import verify_user
from app.infrastructure.security import verify_password, create_access_token
from datetime import timedelta,  datetime
from app.infrastructure.config import settings
from app.exceptions import CustomHTTPException

router = APIRouter()

@router.post("/access-token", response_model=SuccessResponse[LoginResponseData])
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db_dashboard)):
    user = await verify_user(db, request.username)
    
    if not user or not verify_password(request.password, user.password):
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="username or password is incorrect"
        )

    access_token_expires = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires_timestamp = int(access_token_expires.timestamp())
    
    access_token = create_access_token(
        data={"username": user.username, "id": user.id}, 
        expires_at=access_token_expires_timestamp
    )

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=LoginResponseData(
            access_token=access_token,
            token_type="Bearer",
            expires_in=access_token_expires_timestamp
    )
)