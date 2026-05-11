from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    text
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class RolePermissions(Base):

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False
    )

    permission_id = Column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        PrimaryKeyConstraint("role_id", "permission_id"),
    )