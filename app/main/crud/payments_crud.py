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

class CRUDPayment(CRUDBase[models.Payment,schemas.Payment,schemas.PaymentUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Payment).filter(models.Payment.uuid==uuid).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.PaymentCreate.user_uuid):
        payment = models.Payment(
            uuid = str(uuid.uuid4()),
            code = obj_in.code,
            month = obj_in.month,
            montant = obj_in.montant,
            is_total = obj_in.is_total
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.PaymentUpdate):
        payment = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if payment is None:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        code = obj_in.code if obj_in.code else code
        month = obj_in.month if obj_in.month else month
        montant = obj_in.montant if obj_in.montant else montant
        is_total = obj_in.is_total if obj_in.is_total else is_total
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        obj_in = cls.get_by_uuid(db,uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        obj_in.is_active = is_active
        db.commit()

    @classmethod
    def delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db==db,uuid==uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        db.delete(obj_in)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db==db,uuid==uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="payment-not-found"))
        obj_in.is_deleted=True
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page: int = 1,
        per_page: int = 25,
    ):
        record_query = db.query(models.Payment).filter(models.Payment.is_deleted==False)

        total = record_query.count(
        record_query = record_query.offset((page - 1) * per_page)).limit(per_page)
        return schemas.PaymentResponseList(
            total = total,
            pages = math.ceil(total / per_page),
            per_page = per_page,
            current_page = page,
            data = record_query
        )