from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base
from enum import Enum

class CanalReceptionMessage(str, Enum):
    mail = "mail"
    sms = "sms"
    watsapp = "watsapp"


class Messages(Base):

    __tablename__ = 'messages'

    uuid = Column(String, primary_key=True)

    user_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)
    user = relationship("User", foreign_keys=[user_uuid])

    message = Column(String, nullable=False, index=True)

    product_uuid = Column(String, ForeignKey("products.uuid"), nullable=False, index=True)
    product = relationship("Product", foreign_keys=[product_uuid])

    canal_reception = Column(String,default=CanalReceptionMessage.mail,nullable=False)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Messages()uuid={self.uuid}, message={self.message}, product_uuid={self.product_uuid}>"