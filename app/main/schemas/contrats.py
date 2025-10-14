from typing import Optional
from app.main.schemas.user import AddedBy
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Contrat(BaseModel):
    title:str
    clauses:str
    product_uuid:list[str] = None


class ContratCreate(Contrat):
    pass


class ContratUpdate(BaseModel):
    title:Optional[str]
    clauses:Optional[str]
    product_uuid:Optional[list[str]] = None

class ContratResponse(BaseModel):
    title:str
    clauses:str
    product_uuid:list[str] = None
    user:AddedBy

model_config = ConfigDict(from_attributes=True)

class ContratResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Contrat]

    model_config = ConfigDict(from_attributes=True)