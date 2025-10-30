from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_payment(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PaymentsCreate,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):
    product = crud.products.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.payments.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="payment-create-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_payment_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PaymentsUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    if obj_in.status not in [models.PaymentStatus.cancelled, models.PaymentStatus.confirmed, models.PaymentStatus.declined, models.PaymentStatus.pending]:
        raise HTTPException(status_code=404, detail=__(key="invalid-status"))
    crud.payments.update_status(
        db=db,
        uuid=obj_in.uuid,
        status=obj_in.status
    )
    return schemas.Msg(message=__(key="payment-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_payment(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PaymentsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
    
):
    crud.payments.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="payment-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_payment(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PaymentsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
    
):
    crud.payments.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="payment-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = Query(None, enum=[st.value for st in models.PaymentStatus]),
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    return crud.payments.get_all_payments(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
        status=status
    )

