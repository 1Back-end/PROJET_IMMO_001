from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Customer(BaseModel):
    email:str
    phone_number:str
    phone_number_2:str
    first_name:str
    last_name:str
    password:str
    country_uuid:list[str] = None
    city_uuid:list[str] = None


class CustomerCreate(Customer):
    pass


class CustomerUpdate(BaseModel):
    email:Optional[str]
    phone_number:Optional[str]
    phone_number_2:Optional[str]
    first_name:Optional[str]
    last_name:Optional[str]
    password:Optional[str]
    country_uuid:Optional[list[str]] = None
    city_uuid:Optional[list[str]] = None


class CustomerResponse(BaseModel):
    email:str
    phone_number:str
    phone_number_2:str
    first_name:str
    last_name:str
    password:str
    country_uuid:list[str] = None
    city_uuid:list[str] = None
    user:AddedBy

 model_config = ConfigDict(from_attributes=True)

class CustomerResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[User]

    model_config = ConfigDict(from_attributes=True)