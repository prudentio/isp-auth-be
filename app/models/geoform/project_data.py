from sqlalchemy import Column, String, Integer, LargeBinary, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from geoalchemy2 import Geometry
from uuid import uuid4
from app.infrastructure.db.base import Base

class ProjectData(Base):
    id = Column(PGUUID, primary_key=True, default=uuid4)
    geom = Column(Geometry('GEOMETRY'), nullable=False)
    geom_type = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    project_id = Column(PGUUID, nullable=False)
    created_by = Column(PGUUID, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, default=1, nullable=False)
    hash = Column(LargeBinary, nullable=True)
    updated_by = Column(PGUUID, nullable=True)
    participant_location = Column(Geometry('POINT', 4326), nullable=True)
    tag_id = Column(PGUUID, nullable=True)