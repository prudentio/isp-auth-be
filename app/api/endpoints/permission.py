from typing import Annotated, List
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.rabbit_client import publish
from app.infrastructure.db.session import get_db
from app.middleware.jwt_auth import get_current_user
from app.schemas.permission import (
    CreatePermissionRequest,
    PermissionResponse,
    UpdatePermissionRequest,
)
from app.schemas.response import SuccessResponse
from app.exceptions import CustomHTTPException
from app.services.permission import (
    create_permission,
    delete_permission,
    get_many_permissions,
    update_permission
)

router = APIRouter()


@router.get("", response_model=SuccessResponse[List[PermissionResponse]])
async def get_permissions(
    user_id: Annotated[str, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):

    permissions = await get_many_permissions(db)

    if not permissions:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "get permissions failed",
            "endpoint": "/auth/permission",
            "method": "GET",
            "metadata": {
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="failed to get permissions"
        )

    publish("log.events", {
        "service": "role",
        "level": "INFO",
        "message": "list permissions fetched",
        "endpoint": "/auth/permissions",
        "method": "GET",
        "metadata": {
            "user_id": user_id
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=[
            PermissionResponse(id=p.id, code=p.code)
            for p in permissions
        ]
    )


@router.post("", response_model=SuccessResponse[PermissionResponse])
async def create(
    user_id: Annotated[str, Depends(get_current_user)],
    payload: CreatePermissionRequest,
    db: AsyncSession = Depends(get_db),
):

    permission = await create_permission(db, payload)

    if not permission:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "get permission failed",
            "endpoint": "/auth/permission",
            "method": "POST",
            "metadata": {
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="failed to create permission"
        )

    publish("audit.events", {
        "service": "role",
        "module": "permission",
        "action": "CREATE_PERMISSION",
        "description": f"permission {permission.code} created",
        "metadata": {
            "payload": payload,
            "user_id": user_id
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "permission created",
        "endpoint": "/auth/permissions",
        "method": "POST",
        "metadata": {
            "user_id": user_id,
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_201_CREATED,
        data=PermissionResponse(
            id=permission.id,
            code=permission.code
        )
    )


@router.patch("/{permission_id}", response_model=SuccessResponse[PermissionResponse])
async def update(
    user: Annotated[str, Depends(get_current_user)],
    permission_id: uuid.UUID,
    payload: UpdatePermissionRequest,
    db: AsyncSession = Depends(get_db),
):

    permission = await update_permission(db, permission_id, payload)

    if not permission:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "update permission failed",
            "endpoint": "/auth/permission",
            "method": "UPDATE",
            "metadata": {
                "payload": payload,
                "user_id": user,
                "permission_id": permission_id,
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="permission not found"
        )

    publish("audit.events", {
        "service": "auth",
        "module": "permission",
        "action": "UPDATE_PERMISSION",
        "description": f"permission {permission.code} updated",
        "metadata": {
            "payload": payload,
            "user_id": user,
            "permission_id": permission_id,
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "permission updated",
        "endpoint": f"/auth/permissions/{permission_id}",
        "method": "PATCH",
        "metadata": {
            "permission_id": permission_id,
            "user_id": user
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=PermissionResponse(id=permission.id, code=permission.code)
    )


@router.delete("/{permission_id}", response_model=SuccessResponse[dict])
async def delete(
    user: Annotated[str, Depends(get_current_user)],
    permission_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):

    deleted_id = await delete_permission(db, permission_id)

    if not deleted_id:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "delete permission failed",
            "endpoint": "/auth/permission",
            "method": "DELETE",
            "metadata": {
                "deleted_id": deleted_id,
                "user_id": user
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="permission not found"
        )

    publish("audit.events", {
        "service": "auth",
        "module": "permission",
        "action": "DELETE_PERMISSION",
        "description": f"permission {permission_id} deleted",
        "metadata": {
            "user_id": user,
            "permission_id": str(permission_id)
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "WARNING",
        "message": "permission deleted",
        "endpoint": f"/auth/permissions/{permission_id}",
        "method": "DELETE",
        "metadata": {
            "user_id": user
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data={"deleted_id": deleted_id}
    )