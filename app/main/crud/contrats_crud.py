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

class CRUDContrat(CRUDBase[models.Contrats,schemas.Contrat,schemas.ContratUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Contrats).filter(models.Contrats.uuid == uuid).first()
    
    @classmethod
    def create(cls,db:Session, *, obj_in:schemas.ContratCreate):
        product = models.Contrats(
            uuid = str(uuid.uuid4()),
            title = obj_in.title,
            clauses = obj_in.clauses,
            product_uuid = obj_in.product_uuid,
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.ContratUpdate):
        contrat = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if contrat is None:
            raise HTTPException(status_code=404, detail=__(key="contrat-not-found"))
        title = obj_in.title if obj_in.title else title
        clauses = obj_in.clauses if obj_in.clauses else clauses
        product_uuid = obj_in.product_uuid if obj_in.product_uuid else product_uuid
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        obj_in = cls.get_by_uuid(db,uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="contrat-not-found"))
        obj_in.is_active = is_active
        db.commit()

    @classmethod
    def delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db==db,uuid==uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="contrat-not-found"))
        db.delete(obj_in)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db==db,uuid==uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="contrat-not-found"))
        obj_in.is_deleted=True
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page: int = 1,
        per_page: int = 25,
    ):
        record_query = db.query(models.Contrats).filter(models.Contrats.is_deleted==False)

        total = record_query.count(
        record_query = record_query.offset((page - 1) * per_page)).limit(per_page)
        return schemas.ContratResponseList(
            total = total,
            pages = math.ceil(total / per_page),
            per_page = per_page,
            current_page = page,
            data = record_query
        )