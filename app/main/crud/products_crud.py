import math
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session

from app.main.core.mail import send_code_validation
from app.main.core.security import generate_product_code
from app.main.crud.base import CRUDBase
from app.main import models,schemas



class PRODUCT_CRUD(CRUDBase[models.Product,schemas.ProductCreate,schemas.ProductUpdate]):

    @classmethod
    def get_by_code(cls,db:Session, code: str) -> Optional[models.Product]:
        return db.query(models.Product).filter(models.Product.code == code,models.Product.is_deleted==False).first()

    @classmethod
    def get_by_uuid(cls,db:Session, uuid: str) -> Optional[models.Product]:
        return db.query(models.Product).filter(models.Product.uuid == uuid,models.Product.is_deleted==False).first()

    @classmethod
    def create(cls,db:Session,obj_in:schemas.ProductCreate,owner_uuid:str):
        code = generate_product_code()
        product_uuid = str(uuid.uuid4())
        new_product = models.Product(
            uuid = product_uuid,
            code = code,
            name = obj_in.name,
            description = obj_in.description,
            price = obj_in.price,
            mode= obj_in.mode,
            position = obj_in.position,
            owner_uuid = owner_uuid,
        )
        db.add(new_product)
        db.commit()
        for img in obj_in.images:
            new_images = models.ProductImage(
                uuid = str(uuid.uuid4()),
                product_uuid= product_uuid,
                owner_uuid = owner_uuid,
                image_uuid= img.image_uuid
            )
            db.add(new_images)
        db.commit()
        return new_product


    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="product-not-found"))
        db_obj.status = status
        db.commit()


    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def update(cls,db:Session,obj_in:schemas.ProductUpdate,owner_uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.description = obj_in.description if obj_in.description else db_obj.description
        db_obj.price = obj_in.price if obj_in.price else db_obj.price
        db_obj.mode = obj_in.mode if obj_in.mode else db_obj.mode
        db_obj.position = obj_in.position if obj_in.position else db_obj.position
        db_obj.owner_uuid = owner_uuid

        db.query(models.ProductImage).filter(models.ProductImage.uuid == obj_in.uuid).delete()

        for img in obj_in.images:
            new_image = models.ProductImage(
                uuid=str(uuid.uuid4()),
                product_uuid=db_obj.uuid,
                owner_uuid=owner_uuid,
                image_uuid=img.image_uuid
            )
            db.add(new_image)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    @classmethod
    def get_all_data(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status: Optional[str] = None,
            mode :  Optional[str] = None,
            position: Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Product).filter(models.Product.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Product.name.ilike(f'%{keyword}%'),
                    models.Product.description.ilike(f'%{keyword}%'),
                    models.Product.code.ilike(f'%{keyword}%'),
                    models.Product.price.ilike(f'%{keyword}%'),
                )
            )

        if status:
            record_query = record_query.filter(models.Product.status == status)

        if mode:
            record_query = record_query.filter(models.Product.mode == mode)

        if position:
            record_query = record_query.filter(models.Product.position == position)

        if order and order_field and hasattr(models.Product, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Product, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Product, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.ProductResponseResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )

    @classmethod
    def get_by_owner_uuid(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status: Optional[str] = None,
            owner_uuid: Optional[str] = None,
            mode: Optional[str] = None,
            position: Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Product).filter(models.Product.is_deleted == False,models.Product.owner_uuid == owner_uuid)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Product.name.ilike(f'%{keyword}%'),
                    models.Product.description.ilike(f'%{keyword}%'),
                    models.Product.code.ilike(f'%{keyword}%'),
                    models.Product.price.ilike(f'%{keyword}%'),
                )
            )

        if status:
            record_query = record_query.filter(models.Product.status == status)

        if mode:
            record_query = record_query.filter(models.Product.mode == mode)

        if position:
            record_query = record_query.filter(models.Product.position == position)

        if order and order_field and hasattr(models.Product, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Product, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Product, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.ProductResponseResponseListSlim1(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )



products = PRODUCT_CRUD(models.Product)

