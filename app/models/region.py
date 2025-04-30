from sqlalchemy import Column, String
from app.infrastructure.db.base import Base

class Regions(Base):
    id=Column(String, primary_key=True, index = True)
    name=Column(String, nullable=False)
    level=Column(String, nullable=False)
    parent_id = Column(String, nullable=False)
    kd_prov=Column(String, nullable=False)
    kd_kab=Column(String, nullable=True)
    kd_kec=Column(String, nullable=True)
    kd_kel=Column(String, nullable=True)
    kd_rw=Column(String, nullable=True)
    kd_rt=Column(String, nullable=True)
    tag_id = Column(String,nullable=True)