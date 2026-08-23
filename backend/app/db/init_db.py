from sqlalchemy.orm import Session
from app.models.base import Base
from app.db.session import engine
from app.models import *  # Import all models

def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def drop_db():
    """Drop all tables (use with caution)"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped")