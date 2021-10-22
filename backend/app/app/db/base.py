"""
Convenience file that groups all DB models necessary to initialize a DB to
a base minimum working state. To be used with the app/db/init_db.py script
"""
from app.models.model_base import Base 
from app.models.user import User