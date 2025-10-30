from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException,Query
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
    obj_in:schemas.ContratsCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    
    product = crud.products.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.contrats.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="contrats-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_contrats(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    product = crud.products.get_by_uuid(db=db,uuid=obj_in.product_uuid)
    if not product:
        raise HTTPException(status_code=404, detail=__(key="product-not-found"))
    
    crud.contrats.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="contrat-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_contrat_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratsUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    if obj_in.status not in [models.ConntratsSatus.cancelled, models.ConntratsSatus.confirmed, models.ConntratsSatus.pending, models.ConntratsSatus.rejected, models.ConntratsSatus.requested]:
        raise HTTPException(status_code=400, detail=__(key="invalid-status"))
    crud.contrats.update_status(
        db=db,
        uuid=obj_in.uuid,
        status=obj_in.status
    )
    return schemas.Msg(message=__(key="contrat-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_contrats(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
    
):
    crud.contrats.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="contrat-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_contrats(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ContratsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
    
):
    crud.contrats.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="contrat-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = Query(None, enum=[st.value for st in models.ConntratsSatus]),
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    return crud.contrats.get_all_contrats(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
        status=status
    )

@router.get("/get_my_contrat", response_model = None)
async def get_my_contrat(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = Query(None, enum=[st.value for st in models.ConntratsSatus]),
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    return crud.contrats.get_contrats_by_added_by(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
        status=status,
        added_by=current_user.uuid
    )

@router.get("/get_by_uuid", response_model=schemas.ContratsResponse)
async def get_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid: str,
    current_user: models.User = Depends(TokenRequired(roles=["CUSTOMER"]))
):
    data = crud.contrats.get_by_uuid(db=db, uuid=uuid)
    if not data:
        raise HTTPException(status_code=404, detail=__("contrat-not-found"))
    return data