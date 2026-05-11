import uuid
from sqlalchemy import UUID, Column, DateTime, ForeignKey,  Text, text
from app.infrastructure.db.base import Base
from sqlalchemy.orm import relationship

class Users(Base):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    username = Column(
        Text,
        nullable=False,
        unique=True
    )

    password = Column(
        Text,
        nullable=False
    )

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="RESTRICT"),
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

    role = relationship("Roles", back_populates="users")