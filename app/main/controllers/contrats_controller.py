from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/contrats", tags=["contrats"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_contrat(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
        
    exist_uuid = crud.contrat.get_by_uuid(db=db,uuid=obj_in.uuid)
    if exist_uuid:
        raise HTTPException(status_code=409, detail=__(key="contrats-already-exist"))
    
    exist_title = crud.contrats.get_by_title(db=db,title=obj_in.title)
    if exist_title:
        raise HTTPException(status_code=409, detail=__(key="contrats-already-exist"))
    
    product = crud.contrat.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.contrat.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="contrats-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_contrat(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ProductUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_uuid = crud.contrat.uuid(db=db,uuid=obj_in.uuid)
    if exist_uuid:
        raise HTTPException(status_code=409, detail=__(key="uuid-already-exist"))
    
    exist_title = crud.contrat.get_by_title(db=db,title=obj_in.title)
    if exist_title:
        raise HTTPException(status_code=409, detail=__(key="title-already-exist"))
    
    crud.contrat.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="contrat-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_contrat_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.contrat.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="contrat-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_product(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.contrat.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="contrat-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_contrat(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.contrat.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="contrat-deleted-successfully"))

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