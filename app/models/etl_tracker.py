from sqlalchemy import Column, DateTime
from app.infrastructure.db.base import Base

class EtlTracker(Base):
    start_processed_at = Column(DateTime(timezone=True),  primary_key=True,nullable=False)
    end_processed_at = Column(DateTime(timezone=True),  primary_key=True, nullable=False)