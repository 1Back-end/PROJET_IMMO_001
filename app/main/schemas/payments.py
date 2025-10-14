from typing import Optional
from app.main.schemas.user import AddedBy
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Payment(BaseModel):
    code:str
    month:str
    montant:str
    is_total:bool


class PaymentCreate(Payment):
    pass


class PaymentUpdate(BaseModel):
    code:Optional[str]
    month:Optional[str]
    montant:Optional[str]
    is_total:Optional[bool] 

class PaymentResponse(BaseModel):
    code:str
    month:str
    montant:str
    is_total:bool
    user:AddedBy

model_config = ConfigDict(from_attributes=True)

class PaymentResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Payment]

    model_config = ConfigDict(from_attributes=True)