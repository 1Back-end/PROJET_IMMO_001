from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/create",response_model=schemas.Msg)
async def create_customer(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.CustomerCreate
):
    exist_customer_phone_number = crud.customers.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_customer_phone_number:
        raise HTTPException(status_code=409,detail=__(key="customer-phone-number-already-exists"))

    if obj_in.email:
        exist_customer_email = crud.customers.get_by_email(db=db,email=obj_in.email)
        if exist_customer_email:
            raise HTTPException(status_code=409,detail=__(key="customer-email-already-exists"))

    if obj_in.phone_number_2:
        exist_customer_phone_number_2 = crud.customers.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_customer_phone_number_2:
            raise HTTPException(status_code=409,detail=__(key="customer-phone-number-2-already-exists"))

    existe_user_email = crud.user.get_by_email(db=db,email=obj_in.email)
    if existe_user_email:
        raise HTTPException(status_code=409,detail=__(key="user-email-already-exists"))

    exist_user_phone_number = crud.user.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_user_phone_number:
        raise HTTPException(status_code=409,detail=__(key="user-phone-number-already-exists"))

    country = crud.country_with_city.get_country_by_uuid(db=db,uuid=obj_in.country_uuid)
    if not country:
        raise HTTPException(status_code=404,detail=__(key="country-uuid-does-not-exist"))

    city = crud.country_with_city.get_city_by_uuid(db=db,uuid=obj_in.city_uuid)
    if not city:
        raise HTTPException(status_code=404,detail=__(key="city-uuid-does-not-exist"))

    crud.customers.create(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="customer-created-successfully"))



@router.delete("/delete",response_model=schemas.Msg)
async def delete_customer(
        *,
        db: Session = Depends(get_db),
        obj_in : schemas.CustomerDelete
):
    crud.customers.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="customer-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg)
async def soft_delete_customer(
        *,
        db: Session = Depends(get_db),
        obj_in : schemas.CustomerDelete
):
    crud.customers.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="customer-soft-deleted-successfully"))


@router.get("/get_by_uuid",response_model=schemas.CustomerResponse)
async def customers_by_uuid(
        *,
        db: Session = Depends(get_db),
        uuid:str
):
    return crud.customers.get_by_uuid(db=db,uuid=uuid)



@router.put("/validate_account",response_model=schemas.Msg)
async def validate_account(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.CustomerValidationAccount
):
    crud.customers.verify_account(db=db,code=obj_in.code,email=obj_in.email)
    return schemas.Msg(message=__(key="customer-validated-successfully"))


@router.get("/get_all_customers", response_model=None)
async def get_all_customers(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        status: Optional[str] = Query(None, enum=[st.value for st in models.Customer_Status]),
        order_field: Optional[str] = None,
):
    return crud.customers.get_all_data(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        order_field=order_field,

    )