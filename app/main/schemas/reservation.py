from typing import Optional
from app.main.schemas.user import AddedBy
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Reservation(BaseModel):
    product_uuid:list[str] = None


class ReservationCreate(Reservation):
    pass


class ReservationUpdate(BaseModel):
    product_uuid:Optional[list[str]] = None

class ReservationResponse(BaseModel):
    product_uuid:list[str] = None
    user:AddedBy

    model_config = ConfigDict(from_attributes=True)

class ReservationResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Reservation]

    model_config = ConfigDict(from_attributes=True)