from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.main.models.db.base_class import Base


class PaymentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    declined = "declined"
    cancelled = "cancelled"


class Payment(Base):

    __tablename__ = 'payments'

    uuid = Column(String, primary_key=True)
    code = Column(String, nullable=False, index=True)
    month = Column(String, nullable=False, index=True)
    montant = Column(String, nullable=False, index=True)
    is_total = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default=PaymentStatus.pending)
    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)

    user = relationship("User", foreign_keys=[user_uuid])
    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())