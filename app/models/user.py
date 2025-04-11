from sqlalchemy import Column, Integer, String
from app.infrastructure.db.base import Base

class Users(Base):
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)