from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import UserReservation, ProductResponseSlim1, AddedBySlim


class Contrat(BaseModel):
    user_uuid:str
    title:str
    clauses:str
    product_uuid:str


class ContratsCreate(Contrat):
    pass


class ContratUpdate(BaseModel):
    uuid:str
    user_uuid:Optional[str]
    title:Optional[str]
    clauses:Optional[str]
    product_uuid:Optional[str]


class ContratsDelete(BaseModel):
    uuid:str


class ContratsUpdateStatus(BaseModel):
    uuid:str
    status:str

class ContratsResponse(BaseModel):
    uuid:str
    title: str
    clauses: str
    user:UserReservation
    product:ProductResponseSlim1
    creator : AddedBySlim
    model_config = ConfigDict(from_attributes=True)

class ContratsResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[ContratsResponse]

    model_config = ConfigDict(from_attributes=True)


class ContratsResponseSlim1(BaseModel):
    uuid:str
    title: str
    clauses: str
    user:UserReservation
    product:ProductResponseSlim1
    creator : AddedBySlim
    model_config = ConfigDict(from_attributes=True)



class ContratsResponseListSlim1(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[ContratsResponseSlim1]

    model_config = ConfigDict(from_attributes=True)

