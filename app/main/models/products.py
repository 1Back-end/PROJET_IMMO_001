from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.main.models.db.base_class import Base

class ProductMode(str, Enum):
    STANDARD = "standard"
    PREMIUM = "premium"
    VIP = "vip"


class ProductStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class ProductPosition(str, Enum):
    LOCATION = "location"
    SELL = "sell"
    BUY = "buy"


class Product(Base):
    __tablename__ = "products"

    uuid = Column(String, primary_key=True)
    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True, index=True)
    price = Column(String, nullable=False)
    mode = Column(String, nullable=False, default=ProductMode.STANDARD)
    status = Column(String, nullable=False, default=ProductStatus.AVAILABLE)
    position = Column(String, nullable=False, default=ProductPosition.LOCATION)
    is_deleted = Column(Boolean, nullable=False, default=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)
    owner = relationship("User", foreign_keys=[owner_uuid])

    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Product(uuid={self.uuid}, code={self.code}, name={self.name})>"


class ProductImage(Base):
    __tablename__ = "product_images"

    uuid = Column(String, primary_key=True)
    product_uuid = Column(String, ForeignKey("products.uuid"), nullable=False, index=True)
    product = relationship("Product", foreign_keys=[product_uuid])

    owner_uuid = Column(String, ForeignKey("users.uuid"), nullable=False, index=True)
    owner = relationship("User",foreign_keys=[owner_uuid])

    image_uuid = Column(String, ForeignKey("storages.uuid"), nullable=False, index=True)
    image = relationship("Storage", foreign_keys=[image_uuid])

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ProductImage(uuid={self.uuid}, product_uuid={self.product_uuid})>"
