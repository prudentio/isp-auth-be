
from app.schemas.response import CamelModel
from uuid import UUID

class PermissionResponse(CamelModel):
    id: UUID
    code: str


class CreatePermissionRequest(CamelModel):
    code: str


class UpdatePermissionRequest(CamelModel):
    code: str | None = None
