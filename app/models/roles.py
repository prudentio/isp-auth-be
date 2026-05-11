import uuid
from sqlalchemy import Column, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base
from app.models.role_permissions import RolePermissions


class Roles(Base):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    name = Column(
        Text,
        nullable=False,
        unique=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    users = relationship(
        "Users",
        back_populates="role"
    )

    permissions = relationship(
        "Permissions",
        secondary=RolePermissions.__table__,
        back_populates="roles"
    )