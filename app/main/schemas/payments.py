from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import UserReservation, ProductResponseSlim1


class PaymentsBase(BaseModel):
    month:str
    montant:str
    product_uuid:str


class PaymentsCreate(PaymentsBase):
    pass


class PaymentsDelete(BaseModel):
    uuid:str

class PaymentsUpdateStatus(BaseModel):
    uuid:str
    status:str

class PaymentsResponse(BaseModel):
    uuid:str
    month:str
    montant:str
    status:str
    product: ProductResponseSlim1
    user:UserReservation


class PaymentsResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[PaymentsResponse]

    model_config = ConfigDict(from_attributes=True)