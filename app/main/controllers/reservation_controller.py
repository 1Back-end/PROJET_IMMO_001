from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/add_reservation",response_model=schemas.Msg)
async def add_reservation(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.ReservationCreate
):
    product = crud.products.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404,detail=__("product-not-found"))


    exist_user_phone_number = crud.user.get_by_phone_number(db=db, phone_number=obj_in.phone_number)
    if exist_user_phone_number:
        raise HTTPException(status_code=409, detail=__(key="user-phone-number-already-exists"))

    crud.reservations.create(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="reservation-created"))


@router.get("/get_all_reservation", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: Optional[str] = None,
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = Query(None, enum=[st.value for st in models.ReservationStatus]),
):
    return crud.reservations.get_all_reservation(
        db,
        page,
        per_page,
        order,
        order_field,
        keyword,
        status,
    )

