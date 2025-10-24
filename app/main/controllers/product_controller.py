from datetime import timedelta, datetime
from itertools import product
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/create",response_model=schemas.Msg)
async def create_product(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.ProductCreate,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    image_uuids = [img.image_uuid for img in obj_in.images]
    images = crud.storage_crud.get_by_uuids(db=db, uuids=image_uuids)
    if not images or len(images) != len(image_uuids):
        raise HTTPException(status_code=404, detail=__(key="image-not-found"))

    if obj_in.mode not in [models.ProductMode.PREMIUM,models.ProductMode.VIP,models.ProductMode.STANDARD]:
        raise HTTPException(status_code=400, detail=__(key="invalid-mode"))

    if obj_in.position not in [models.ProductPosition.BUY,models.ProductPosition.SELL,models.ProductPosition.LOCATION]:
        raise HTTPException(status_code=400, detail=__(key="invalid-position"))


    crud.products.create(db=db, obj_in=obj_in,owner_uuid=current_user.uuid)
    return schemas.Msg(message=__(key="product-created"))


@router.put("/update",response_model=schemas.Msg)
async def update_product(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.ProductUpdate,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    image_uuids = [img.image_uuid for img in obj_in.images]
    images = crud.storage_crud.get_by_uuids(db=db, uuids=image_uuids)
    if not images or len(images) != len(image_uuids):
        raise HTTPException(status_code=404, detail=__(key="image-not-found"))

    if obj_in.mode not in [models.ProductMode.PREMIUM, models.ProductMode.VIP, models.ProductMode.STANDARD]:
        raise HTTPException(status_code=400, detail=__(key="invalid-mode"))

    if obj_in.position not in [models.ProductPosition.BUY, models.ProductPosition.SELL,
                               models.ProductPosition.LOCATION]:
        raise HTTPException(status_code=400, detail=__(key="invalid-position"))

    crud.products.update(db=db, obj_in=obj_in, owner_uuid=current_user.uuid)
    return schemas.Msg(message=__(key="product-updated"))


@router.delete("/delete",response_model=schemas.Msg)
async def delete_product(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.ProductDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    product = crud.products.get_by_uuid(db=db, uuid=obj_in.uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    if current_user.uuid != product.owner_uuid:
        raise HTTPException(status_code=403, detail=__(key="not-authorized"))
    crud.products.delete(db=db, obj_in=obj_in)
    return schemas.Msg(message=__(key="product-deleted"))


@router.put("/soft_delete",response_model=schemas.Msg)
async def soft_delete_product(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.ProductDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    product = crud.products.get_by_uuid(db=db, uuid=obj_in.uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    if current_user.uuid != product.owner_uuid:
        raise HTTPException(status_code=403, detail=__(key="not-authorized"))
    crud.products.soft_delete(db=db, obj_in=obj_in)
    return schemas.Msg(message=__(key="product-deleted"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_status_product(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.ProductUpdateStatus,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    product = crud.products.get_by_uuid(db=db, uuid=obj_in.uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    if current_user.uuid != product.owner_uuid:
        raise HTTPException(status_code=403, detail=__(key="not-authorized"))
    if obj_in.status not in [models.ProductStatus.AVAILABLE,models.ProductStatus.UNAVAILABLE]:
        raise HTTPException(status_code=400, detail=__(key="invalid-status"))
    crud.products.update_status(db=db, obj_in=obj_in, status=obj_in.status)
    return schemas.Msg(message=__(key="product-updated-status"))


@router.get("/get_all_products", response_model=None)
async def get_all_products(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        status: Optional[str] = Query(None, enum=[st.value for st in models.ProductStatus]),
        mode: Optional[str] = Query(None, enum=[st.value for st in models.ProductMode]),
        position: Optional[str] = Query(None, enum=[st.value for st in models.ProductPosition]),
        order_field: Optional[str] = None,
):
    return crud.products.get_all_data(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        mode=mode,
        position=position,
        order_field=order_field,

    )


@router.get("/get_all_products_by_owner_uuid", response_model=None)
async def get_all_products_by_owner_uuid(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        status: Optional[str] = Query(None, enum=[st.value for st in models.ProductStatus]),
        mode: Optional[str] = Query(None, enum=[st.value for st in models.ProductMode]),
        position: Optional[str] = Query(None, enum=[st.value for st in models.ProductPosition]),
        order_field: Optional[str] = None,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    return crud.products.get_by_owner_uuid(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        mode=mode,
        position=position,
        order_field=order_field,
        owner_uuid=current_user.uuid,

    )


@router.get("/get_by_uuid",response_model=schemas.ProductResponse)
async def get_by_uuid(
        *,
        db: Session = Depends(get_db),
        uuid: str,
        current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER","ADMIN","SUPER_ADMIN"]))
):
    data = crud.customers.get_by_uuid(db=db, uuid=uuid)
    if not data:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    return data