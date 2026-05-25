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
from app.infrastructure.config import settings
import httpx

router = APIRouter()

@router.get("/access-token")
async def get_arcgis_access_token(
    user_id: Annotated[str, Depends(get_current_user)],
):
    url = "https://www.arcgis.com/sharing/rest/oauth2/token"

    payload = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload)

    if response.status_code != 200:
        publish("log.events", {
            "service": "auth",
            "level": "INFO",
            "message": "failed to get arcgis access token",
            "endpoint": "/arcgis/access-token",
            "method": "GET",
            "metadata": {
                "user_id": str(user_id),
            }
        })

        raise CustomHTTPException(
            status_code=500,
            message="Failed to get ArcGIS access token"
        )

    data = response.json()

    publish("audit.events", {
        "service": "auth",
        "module": "arcgistoken",
        "action": "GET_ARCGIS_ACCESS_TOKEN",
        "description": f"arcgis access token",
        "metadata": {
            "user_id": str(user_id),
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "get arcgis access token",
        "endpoint": "/arcgis/access-token",
        "method": "GET",
        "metadata": {
            "user_id": str(user_id),
        }
    })


    return SuccessResponse(
        status_code=200,
        data={
            "accessToken": data["access_token"],
            "expiresIn": data.get("expires_in"),
        }
    )