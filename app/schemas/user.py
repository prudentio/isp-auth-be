import uuid
from app.schemas.response import CamelModel
from app.schemas.role import RoleResponse

class CreateUserRequest(CamelModel):
    username: str
    password: str
    role_id: uuid.UUID


class UpdateUserRequest(CamelModel):
    username: str | None = None
    password: str | None = None
    role_id: uuid.UUID | None = None


class UserResponse(CamelModel):
    id: uuid.UUID
    username: str
    role: RoleResponse
