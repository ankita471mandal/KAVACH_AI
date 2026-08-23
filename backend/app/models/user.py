from sqlalchemy import Column, Integer, String, Boolean
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), default="citizen")  # admin, authority, rescue_team, citizen, hospital_staff, shelter_manager
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String(255), nullable=False)