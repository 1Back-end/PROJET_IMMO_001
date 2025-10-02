from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base


class ConntratsSatus(str,Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    rejected = 'rejected'
    requested = 'requested'

class Contrats(Base):

    __tablename__ = 'contrats'

    uuid = Column(String, primary_key=True, index=True)

    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)
    user = relationship("User", foreign_keys=[user_uuid])

    title = Column(String, nullable=False, index=True)

    clauses = Column(Text, nullable=False, index=True)

    product_uuid = Column(String, ForeignKey("products.uuid"), nullable=False, index=True)
    product = relationship("Product", foreign_keys=[product_uuid])

    status = Column(String, default=ConntratsSatus.pending, nullable=False)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
