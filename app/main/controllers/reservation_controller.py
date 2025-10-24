from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/reservation", tags=["reservation"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_reservation(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ReservationCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
        
    exist_uuid = crud.reservation.get_by_uuid(db=db,uuid=obj_in.uuid)
    if exist_uuid:
        raise HTTPException(status_code=409, detail=__(key="reservation-already-exist"))
    
    product = crud.product.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.reservation.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="reservation-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_reservation(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ReservationUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_uuid = crud.reservation.uuid(db=db,uuid=obj_in.uuid)
    if exist_uuid:
        raise HTTPException(status_code=409, detail=__(key="uuid-already-exist"))
    
    product = crud.product.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.reservation.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="reservation-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_reservation_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ReservationUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.reservation.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="reservation-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_Reservation(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ReservationDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.reservation.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="reservation-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_Reservation(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ReservationDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.reservation.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="reservation-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.reservation.get_many(
        db=db,
        page=page,
        per_page=per_page
    )