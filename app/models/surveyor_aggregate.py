from sqlalchemy import Column, String, Integer, Date, ForeignKey
from app.infrastructure.db.base import Base

class SurveyorAggregates(Base):
    id=Column(Integer, primary_key=True, nullable=False)
    date=Column(Date, nullable=False)
    surveyor_id = Column(String, nullable=False)
    surveyor_name = Column(String, nullable=False)
    rt_id = Column(String, ForeignKey('regions.id'), nullable=False)
    total_data = Column(Integer, nullable=False)