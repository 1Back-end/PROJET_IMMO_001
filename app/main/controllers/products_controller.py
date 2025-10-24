from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_product(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
        
    exist_uuid = crud.product.get_by_uuid(db=db,uuid=obj_in.uuid)
    if exist_uuid:
        raise HTTPException(status_code=409, detail=__(key="product-already-exist"))
    
    product = crud.product.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.product.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="product-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_product(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_uuid = crud.product.uuid(db=db,uuid=obj_in.uuid)
    if exist_uuid:
        raise HTTPException(status_code=409, detail=__(key="uuid-already-exist"))
    
    exist_code = crud.product.code(db=db,code=obj_in.code)
    if exist_code:
        raise HTTPException(status_code=409, detail=__(key="code-already-exist"))
    
    exist_name = crud.product.name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="name-already-exist"))
    
    image = crud.product.get_by_uuid(db=db,uuid=obj_in.image_uuid)
    if not image:
        raise HTTPException(status_code=404, detail=__(key="image-not-found"))
    
    crud.product.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="product-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_product_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.product.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="product-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_product(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.product.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="product-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_product(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.product.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="product-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.product.get_many(
        db=db,
        page=page,
        per_page=per_page
    )