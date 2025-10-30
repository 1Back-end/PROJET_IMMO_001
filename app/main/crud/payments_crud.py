import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session

from app.main.core.security import generate_payment_code
from app.main.crud import reservations, products
from app.main.crud.base import CRUDBase
from app.main import models,schemas,crud


class CRUD_PAYMENTS(CRUDBase[models.Payment,schemas.PaymentsResponse,schemas.PaymentsCreate]):


    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str) -> Optional[models.Payment]:
        return db.query(models.Payment).filter(models.Payment.uuid == uuid,models.Payment.is_deleted==False).first()

    @classmethod
    def get_by_code(cls,db:Session,code:str) -> Optional[models.Payment]:
        return db.query(models.Payment).filter(models.Payment.code == code,models.Payment.is_deleted==False).first()

    @classmethod
    def create(cls,db:Session,obj_in:schemas.PaymentsCreate,user_uuid:str) -> Optional[models.Payment]:
        code = generate_payment_code()

        product = crud.products.get_by_uuid(db=db,uuid=obj_in.product_uuid)
        if not product:
            raise HTTPException(status_code=404,detail=__(key="product-not-found"))
        is_total = obj_in.montant == product.price

        db_obj = models.Payment(
            uuid=str(uuid.uuid4()),
            code=code,
            month = obj_in.month,
            montant=obj_in.montant,
            user_uuid=user_uuid,
            product_uuid=obj_in.product_uuid,
            is_total = is_total,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str) -> Optional[models.Payment]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        db_obj.status = status
        db.commit()


    @classmethod
    def delete(cls,db:Session,uuid:str) -> Optional[models.Payment]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        db.delete(db_obj)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str) -> Optional[models.Payment]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def get_all_payments(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status: Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Payment).filter(models.Payment.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Payment.code.ilike(f'%{keyword}%'),
                    models.Payment.montant.ilike(f'%{keyword}%'),
                    models.Payment.month.ilike(f'%{keyword}%')
                )
            )

        if status:
            record_query = record_query.filter(models.Payment.status == status)

        if order and order_field and hasattr(models.Payment, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Payment, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Payment, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.PaymentsResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


payments = CRUD_PAYMENTS(models.Payment)
