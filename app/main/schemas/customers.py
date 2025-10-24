from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import CountrySlim1, CitySlim1


class Customers(BaseModel):
    email:Optional[str] = None
    phone_number:str
    phone_number_2 : Optional[str]
    first_name:str
    last_name:str
    country_uuid:str
    city_uuid : str
    password:str


class CustomerCreate(Customers):
    pass


class CustomerUpdate(BaseModel):
    email: Optional[str]
    phone_number: Optional[str]
    phone_number_2: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    country_uuid: Optional[str]
    city_uuid: Optional[str]


class CustomerDelete(BaseModel):
    uuid:str


class CustomerValidationAccount(BaseModel):
    email:str
    code:str


class CustomerResponse(BaseModel):
    uuid:str
    email: str
    phone_number: str
    phone_number_2: str
    first_name: str
    last_name: str
    country: CountrySlim1
    city: CitySlim1
    model_config = ConfigDict(from_attributes=True)



class CustomerResponseResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[CustomerResponse]

    model_config = ConfigDict(from_attributes=True)
