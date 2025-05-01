from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.infrastructure.db.base import Base

class UserAccount(Base):
    id = Column(PGUUID, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable = False)
    created_at = Column(DateTime, nullable = False)
    deleted_at = Column(DateTime, nullable=False)