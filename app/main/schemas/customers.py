from typing import Optional
from app.main.schemas.user import AddedBy
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas import CountrySlim1, CitySlim1

class Customer(BaseModel):
    email:str
    phone_number:str
    phone_number_2:str
    first_name:str
    last_name:str
    password:str
    country_uuid: str
    city_uuid: str


class CustomerCreate(Customer):
    pass


class CustomerUpdate(BaseModel):
    email: Optional[str]
    phone_number: Optional[str]
    phone_number_2: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    country_uuid: Optional[str] = None
    city_uuid: Optional[str] = None


class CustomerResponse(BaseModel):
    email: str
    phone_number: str
    phone_number_2: str
    first_name: str
    last_name: str
    password: str
    country: CountrySlim1
    city: CitySlim1
    user: AddedBy

    model_config = ConfigDict(from_attributes=True)

class CustomerResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[CustomerResponse]

    model_config = ConfigDict(from_attributes=True)

class CustomerValidationAccount(BaseModel):
    email:str
    code:str