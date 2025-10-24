from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class ValidationAccount(Base):
    __tablename__ = 'validation_accounts'

    uuid = Column(String, primary_key=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    is_used = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    expirat_at = Column(DateTime, default=func.now(),nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())