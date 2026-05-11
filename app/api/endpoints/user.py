from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, status
from app.infrastructure.db.session import get_db
from app.middleware.jwt_auth import get_current_user
from app.schemas.response import SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import CustomHTTPException
from app.schemas.user import CreateUserRequest, UpdateUserRequest, UserResponse 
from app.services.role import get_role_by_id
from app.services.user import create_user, delete_user, get_user_by_id, get_users, update_user
from app.utils.rabbit_client import publish

router = APIRouter()

@router.get("")
async def get_users_route(    
    user_id: Annotated[str, Depends(get_current_user)], 
    db: AsyncSession = Depends(get_db)
):
    users = await get_users(db)

    if not users:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "get users failed",
            "endpoint": "/auth/users",
            "method": "GET",
            "metadata": {
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="failed to get users"
        )

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "list users fetched",
        "endpoint": "/auth/users",
        "method": "GET",
        "metadata": {
            "user_id": user_id
        }
    })

    return SuccessResponse(
        status_code=200,
        data=[
            UserResponse.model_validate(user)
            for user in users
        ]
    )
    
@router.get("/{user_id}")
async def get_user_by_id_route(
    user: Annotated[str, Depends(get_current_user)], 
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    user_data = await get_user_by_id(db, user_id)

    if not user_data:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "get user by id failed",
            "endpoint": f"/auth/users/{user_id}",
            "method": "GET",
            "metadata": {
                "user_id": user,
                "target_user_id": str(user_id)
            }
        })

        raise CustomHTTPException(
            status_code=404,
            message="user not found"
        )

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "user fetched",
        "endpoint": f"/auth/users/{user_id}",
        "method": "GET",
        "metadata": {
            "user_id": user,
            "target_user_id": str(user_id)
        }
    })

    return SuccessResponse(
        status_code=200,
        data=UserResponse.model_validate(user_data)
    ) 

@router.post("")
async def create_user_route(
    user: Annotated[str, Depends(get_current_user)], 
    payload: CreateUserRequest,
    db: AsyncSession = Depends(get_db)
):
    role = await get_role_by_id(db, payload.role_id)

    if not role:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "create user failed - role not found",
            "endpoint": "/auth/users",
            "method": "POST",
            "metadata": {
                "user_id": user,
                "role_id": str(payload.role_id)
            }
        })

        raise CustomHTTPException(404, "role not found")

    new_user = await create_user(
        db,
        payload.username,
        payload.password,
        payload.role_id,
    )

    publish("audit.events", {
        "service": "auth",
        "module": "user",
        "action": "CREATE_USER",
        "description": f"user {new_user.username} created",
        "metadata": {
            "user_id": user,
            "created_user_id": str(new_user.id)
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "user created",
        "endpoint": "/auth/users",
        "method": "POST",
        "metadata": {
            "user_id": user,
            "created_user_id": str(new_user.id)
        }
    })

    return SuccessResponse(
        status_code=201,
        data=UserResponse.model_validate(new_user)
    )
    
@router.patch("/{user_id}")
async def update_user_route(
    user: Annotated[str, Depends(get_current_user)], 
    user_id: uuid.UUID,
    payload: UpdateUserRequest,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_user(
        db,
        user_id,
        payload.username,
        payload.password,
        payload.role_id,
    )

    if not updated:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "update user failed",
            "endpoint": f"/auth/users/{user_id}",
            "method": "PATCH",
            "metadata": {
                "user_id": user,
                "target_user_id": str(user_id)
            }
        })

        raise CustomHTTPException(404, "user not found")

    publish("audit.events", {
        "service": "auth",
        "module": "user",
        "action": "UPDATE_USER",
        "description": f"user {user_id} updated",
        "metadata": {
            "user_id": user,
            "target_user_id": str(user_id)
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "user updated",
        "endpoint": f"/auth/users/{user_id}",
        "method": "PATCH",
        "metadata": {
            "user_id": user,
            "target_user_id": str(user_id)
        }
    })

    return SuccessResponse(
        status_code=200,
        data="updated"
    )
    
@router.delete("/{user_id}")
async def delete_user_route(
    user: Annotated[str, Depends(get_current_user)], 
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    deleted = await delete_user(db, user_id)

    if not deleted:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "delete user failed",
            "endpoint": f"/auth/users/{user_id}",
            "method": "DELETE",
            "metadata": {
                "user_id": user,
                "target_user_id": str(user_id)
            }
        })

        raise CustomHTTPException(404, "user not found")

    publish("audit.events", {
        "service": "auth",
        "module": "user",
        "action": "DELETE_USER",
        "description": f"user {user_id} deleted",
        "metadata": {
            "user_id": user,
            "target_user_id": str(user_id)
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "WARNING",
        "message": "user deleted",
        "endpoint": f"/auth/users/{user_id}",
        "method": "DELETE",
        "metadata": {
            "user_id": user,
            "target_user_id": str(user_id)
        }
    })

    return SuccessResponse(
        status_code=200,
        data="deleted"
    )