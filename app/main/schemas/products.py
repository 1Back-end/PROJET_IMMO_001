from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import FileSlim, AddedBy, FileSlim1


class ProductImageResponse(BaseModel):
    uuid: str
    image: FileSlim1

    model_config = ConfigDict(from_attributes=True)

class ImageCreate(BaseModel):
    image_uuid : str


class Product(BaseModel):
    name : str
    description : Optional[str]
    price : str
    mode : str
    position : str
    images: Optional[List[ImageCreate]] = []



class ProductCreate(Product):
    pass


class ProductUpdate(BaseModel):
    uuid:str
    name : Optional[str]
    description : Optional[str]
    price : Optional[str]
    mode : Optional[str]
    position : Optional[str]
    images: Optional[List[ImageCreate]] = []


class ProductDelete(BaseModel):
    uuid:str


class ProductUpdateStatus(BaseModel):
    uuid:str
    status : str


class ProductResponse(BaseModel):
    uuid:str
    name: str
    description: Optional[str]
    price: str
    mode: str
    position: str
    status:str
    images: Optional[List[ProductImageResponse]] = []
    owner : AddedBy
    model_config = ConfigDict(from_attributes=True)


class ProductResponseResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ProductResponse]

    model_config = ConfigDict(from_attributes=True)


class ProductResponseSlim1(BaseModel):
    uuid:str
    name: str
    description: Optional[str]
    price: str
    mode: str
    position: str
    status : str
    images: Optional[List[ProductImageResponse]] = []
    model_config = ConfigDict(from_attributes=True)


class ProductResponseResponseListSlim1(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ProductResponseSlim1]

    model_config = ConfigDict(from_attributes=True)