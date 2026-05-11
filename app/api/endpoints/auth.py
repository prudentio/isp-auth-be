from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime
from app.infrastructure.db.session import get_db
from app.middleware.jwt_auth import get_current_user
from app.schemas.auth import LoginRequest, LoginResponseData
from app.schemas.response import SuccessResponse
from app.schemas.user import UserResponse
from app.services.auth import verify_user
from app.infrastructure.security import verify_password, create_access_token
from app.infrastructure.config import settings
from app.exceptions import CustomHTTPException
from app.services.user import get_user_by_id
from app.utils.rabbit_client import publish

router = APIRouter()


@router.post("/access-token", response_model=SuccessResponse[LoginResponseData])
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):

    user = await verify_user(db, request.username)

    if not user or not verify_password(request.password, user.password):
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "login failed",
            "endpoint": "/access-token",
            "method": "POST",
            "metadata": {
                "username": request.username
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="username or password is incorrect"
        )

    access_token_expires = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token_expires_timestamp = int(access_token_expires.timestamp())

    permissions = [
        p.code
        for p in user.role.permissions
    ]


    access_token = create_access_token(
        data={
            "id": str(user.id),
            "username": user.username,
            "role": user.role.name,
            "permissions": permissions,
        },
        expires_at=access_token_expires_timestamp
    )

    publish("audit.events", {
        "service": "auth",
        "module": "login",
        "action": "LOGIN_SUCCESS",
        "description": f"user {user.username} login success",
        "metadata": {
            "user_id": str(user.id),
            "username": user.username
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "login success",
        "endpoint": "/access-token",
        "method": "POST",
        "metadata": {
            "username": user.username
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=LoginResponseData(
            access_token=access_token,
            token_type="Bearer",
            expires_in=access_token_expires_timestamp
        )
    )


@router.get("/userinfo")
async def get_user_info(
    user_id: Annotated[str, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):

    user = await get_user_by_id(db, user_id)

    publish("audit.events", {
        "service": "auth",
        "module": "userinfo",
        "action": "GET_USERINFO",
        "description": f"user {user.username} accessed userinfo",
        "metadata": {
            "user_id": str(user.id),
            "username": user.username
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "get userinfo success",
        "endpoint": "/userinfo",
        "method": "GET",
        "metadata": {
            "user_id": str(user.id),
            "username": user.username
        }
    })

    return SuccessResponse(
        status_code=200,
        data=UserResponse.model_validate(user)
    )