from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import UserReservation, ProductResponseSlim1


class Reservation(BaseModel):
    product_uuid : str
    message : str
    full_name : str
    phone_number : str
    address : str


class ReservationCreate(Reservation):
    pass


class ReservationResponse(BaseModel):
    uuid:str
    message: str
    status: str
    user : UserReservation
    product :ProductResponseSlim1
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)



class ReservationResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ReservationResponse]

    model_config = ConfigDict(from_attributes=True)


class ReservationDelete(BaseModel):
    uuid: str



class ReservationUpdateStatus(BaseModel):
    uuid: str
    status: str


