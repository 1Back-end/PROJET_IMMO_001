import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas

class CRUDProduct(CRUDBase[models.Product,schemas.Product,schemas.ProductUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Product).filter(models.Product.uuid == uuid).first()
    
    @classmethod
    def create(cls,db:Session, *, obj_in:schemas.ProductCreate):
        product = models.Product(
            uuid = str(uuid.uuid4()),
            code = obj_in.code,
            name = obj_in.name,
            description = obj_in.description,
            price = obj_in.price,
            position = obj_in.position,
            image_uuid = obj_in.image_uuid
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.ProductUpdate):
        product = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if product is None:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        code = obj_in.code if obj_in.code else code
        name = obj_in.name if obj_in.name else name
        description = obj_in.description if obj_in.description else description
        price = obj_in.price if obj_in.price else price
        position = obj_in.position if obj_in.position else position
        image_uuid = obj_in.image_uuid if obj_in.image_uuid else image_uuid
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        obj_in = cls.get_by_uuid(db,uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        obj_in.is_active = is_active
        db.commit()

    @classmethod
    def delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db==db,uuid==uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        db.delete(obj_in)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db==db,uuid==uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        obj_in.is_deleted=True
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page: int = 1,
        per_page: int = 25,
    ):
        record_query = db.query(models.Product).filter(models.Product.is_deleted==False)

        total = record_query.count(
        record_query = record_query.offset((page - 1) * per_page)).limit(per_page)
        return schemas.ProductResponseList(
            total = total,
            pages = math.ceil(total / per_page),
            per_page = per_page,
            current_page = page,
            data = record_query
        )
    
products = ProductCRUD(models.Product)