from typing import Optional
from app.main.schemas.user import AddedBy
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Product(BaseModel):
    code:str
    name:str
    description:str
    price:str
    mode:str
    position:str
    image_uuid:list[str] = None


class ProductCreate(Product):
    pass


class ProductUpdate(BaseModel):
    code:Optional[str]
    name:Optional[str]
    description:Optional[str]
    price:Optional[str]
    mode:Optional[str]
    position:Optional[str]
    image_uuid:Optional[list[str]] = None

class ProductResponse(BaseModel):
    code:str
    name:str
    description:str
    price:str
    mode:str
    position:str
    image_uuid:list[str] = None
    owner:AddedBy

model_config = ConfigDict(from_attributes=True)

class ProductResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Product]

    model_config = ConfigDict(from_attributes=True)