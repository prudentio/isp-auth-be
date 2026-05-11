from typing import List
from uuid import UUID

from app.schemas.permission import PermissionResponse
from app.schemas.response import CamelModel


class RoleResponse(CamelModel):
    id: UUID
    name: str
    permissions: List[PermissionResponse]


class CreateRoleRequest(CamelModel):
    name: str
    permission_ids: List[UUID]

class UpdateRolePermissionsRequest(CamelModel):
    permission_ids:  list[UUID]

