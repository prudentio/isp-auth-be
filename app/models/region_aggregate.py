from sqlalchemy import Column, String, Integer, Date, Computed
from app.infrastructure.db.base import Base

class RegionAggregates(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    kec_id = Column(String, Computed("substr(rt_id, 1, 7)", persisted=True), nullable=True) 
    kel_id = Column(String, Computed("substr(rt_id, 1, 10)", persisted=True), nullable=True)
    rw_id = Column(String, Computed("substr(rt_id, 1, 13)", persisted=True), nullable=True)
    rt_id = Column(String, nullable=False)
    total_data = Column(Integer, nullable=False)
