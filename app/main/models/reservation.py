from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.main.models.db.base_class import Base



class ReservationStatus(str,Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"


class Reservation(Base):

    __tablename__ = 'reservations'
    uuid = Column(String, primary_key=True, unique=True)

    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)
    user = relationship("User", foreign_keys=[user_uuid])

    product_uuid = Column(String, ForeignKey("products.uuid"), nullable=False, index=True)
    product = relationship("Product", foreign_keys=[product_uuid])


    status = Column(String, nullable=False, default=ReservationStatus.pending)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Reservation(uuid={self.uuid}, message={self.product_uuid}, status={self.status})>"


