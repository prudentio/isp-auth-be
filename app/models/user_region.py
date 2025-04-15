from sqlalchemy import Column, Integer, ForeignKey, String
from app.infrastructure.db.base import Base
from sqlalchemy.orm import relationship

class UserRegions(Base):
     id=Column(Integer, primary_key=True, index = True)
     user_id=Column(Integer, ForeignKey('users.id'), nullable=False)
     region_id=Column(String, ForeignKey('regions.id'), nullable=False)
     
     user=relationship("Users", backref="user_regions")
     region =relationship("Regions", backref="user_regions")
