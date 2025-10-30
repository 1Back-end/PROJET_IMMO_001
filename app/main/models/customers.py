from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base



class CustomerList(str, Enum):
    agent_immobilier = "agent_immobilier"
    bailleur = "bailleur"
    client = "client"



class Customer_Status(str, Enum):
    active = "active"
    inactive = "inactive"
    closed = "closed"


class Customer(Base):

    __tablename__ = "customers"


    uuid = Column(String, primary_key=True,index=True)

    email = Column(String, index=True, nullable=True)
    phone_number = Column(String(20), nullable=False, default="", index=True)
    phone_number_2 = Column(String(20), nullable=True, default="", index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)

    country_uuid = Column(String, ForeignKey("countries.uuid", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    country = relationship("Country", back_populates="customers")


    city_uuid = Column(String, ForeignKey("cities.uuid",ondelete="SET NULL",onupdate="CASCADE"), nullable=False)
    city = relationship("City", back_populates="customers")

    is_deleted = Column(Boolean, nullable=True, index=True, default=False)

    status = Column(String,nullable=False,default=Customer_Status.inactive)


    is_active = Column(Boolean, nullable=True, index=True, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Customer('{self.first_name} {self.last_name}', '{self.email}')"