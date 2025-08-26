from sqlalchemy import Column, String
from app.infrastructure.db.base import Base

class FamilyCards(Base):
    id = Column(String, primary_key=True, nullable=False)