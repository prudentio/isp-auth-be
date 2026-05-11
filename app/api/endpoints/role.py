from typing import Annotated, List
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_db
from app.middleware.jwt_auth import get_current_user
from app.models.roles import Roles
from app.models.permissions import Permissions
from app.schemas.permission import PermissionResponse
from app.schemas.response import SuccessResponse
from app.utils.rabbit_client import publish
from app.exceptions import CustomHTTPException
from app.schemas.role import CreateRoleRequest, RoleResponse, UpdateRolePermissionsRequest
from app.services.role import create_role, delete_role, get_role_by_id, get_roles, update_role_permissions

router = APIRouter()


@router.get("", response_model=SuccessResponse[List[RoleResponse]])
async def get_roles_route(
    user_id: Annotated[str, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):

    roles = await get_roles(db)

    if not roles:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "get roles failed",
            "endpoint": "/auth/roles",
            "method": "GET",
            "metadata": {
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="failed to get roles"
        )

    publish("log.events", {
        "service": "roles",
        "level": "INFO",
        "message": "list roles fetched",
        "endpoint": "/auth/role",
        "method": "GET",
        "metadata": {
            "user_id": user_id
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=[
            RoleResponse(
                id=r.id,
                name=r.name,
                permissions=[
                    PermissionResponse(
                        id=p.id,
                        code=p.code
                    )
                    for p in r.permissions
                ]
            )
            for r in roles
        ]
    )


@router.post("", response_model=SuccessResponse[RoleResponse])
async def create_role_route(
    user_id: Annotated[str, Depends(get_current_user)],
    payload: CreateRoleRequest,
    db: AsyncSession = Depends(get_db),
):

    role = await create_role(db, payload)

    if not role:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "create role failed",
            "endpoint": "/auth/role",
            "method": "POST",
            "metadata": {
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="failed to create role"
        )

    publish("audit.events", {
        "service": "auth",
        "module": "role",
        "action": "CREATE_ROLE",
        "description": f"role {role.id} created",
        "metadata": {
            "payload": payload,
            "user_id": user_id
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "role created",
        "endpoint": "/auth/role",
        "method": "POST",
        "metadata": {
            "user_id": user_id,
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_201_CREATED,
        data=RoleResponse(
            id=role.id,
            name=role.name,
            permissions=[
                PermissionResponse(
                    id=p.id,
                    code=p.code
                )
                for p in role.permissions
            ]
        )
    )


@router.patch("/{role_id}/permissions", response_model=SuccessResponse[RoleResponse])
async def update_role_permissions_route(
    user_id: Annotated[str, Depends(get_current_user)],
    role_id: uuid.UUID,
    payload: UpdateRolePermissionsRequest,
    db: AsyncSession = Depends(get_db),
):

    role = await get_role_by_id(db, role_id)

    if not role:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "update role failed",
            "endpoint": "/auth/role",
            "method": "UPDATE",
            "metadata": {
                "payload": payload,
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="role not found"
        )

    role = await update_role_permissions(db, role_id, payload.permission_ids)

    publish("audit.events", {
        "service": "auth",
        "module": "role",
        "action": "UPDATE_ROLE",
        "description": f"role {role_id} updated",
        "metadata": {
            "payload": payload,
            "user_id": user_id
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "INFO",
        "message": "role updated",
        "endpoint": f"/auth/role/{role_id}",
        "method": "PATCH",
        "metadata": {
            "user_id": user_id
        }
    })

    return SuccessResponse(
        status_code=status.HTTP_200_OK,
        data=RoleResponse(
            id=role.id,
            name=role.name,
            permissions=[
                PermissionResponse(
                    id=p.id,
                    code=p.code
                )
                for p in role.permissions
            ]
        )
    )


@router.delete("/{role_id}")
async def delete_role_route(
    user_id: Annotated[str, Depends(get_current_user)],
    role_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):

    deleted_id = await delete_role(db, role_id)

    if not deleted_id:
        publish("log.events", {
            "service": "auth",
            "level": "WARNING",
            "message": "delete role failed",
            "endpoint": "/auth/role",
            "method": "DELETE",
            "metadata": {
                "deleted_id": deleted_id,
                "user_id": user_id
            }
        })

        raise CustomHTTPException(
            status_code=404,
            message="role not found"
        )

    publish("audit.events", {
        "service": "auth",
        "module": "role",
        "action": "DELETE_role",
        "description": f"role {role_id} deleted",
        "metadata": {
            "user_id": user_id,
            "role_id": str(role_id)
        }
    })

    publish("log.events", {
        "service": "auth",
        "level": "WARNING",
        "message": "role deleted",
        "endpoint": f"/auth/roles/{role_id}",
        "method": "DELETE",
        "metadata": {
            "user_id": user_id
        }
    })

    return SuccessResponse(
        status_code=200,
        data={"deleted_id": deleted_id}
    )