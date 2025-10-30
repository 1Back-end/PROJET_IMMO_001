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



class CRUD_CONTRATS(CRUDBase[models.Contrats,schemas.ContratsCreate,schemas.ContratUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str) -> Optional[models.Contrats]:
        return db.query(models.Contrats).filter(models.Contrats.uuid == uuid,models.Contrats.is_deleted==False).first()


    @classmethod
    def create(cls,db:Session,obj_in:schemas.ContratsCreate,added_by:str) -> Optional[models.Contrats]:
        db_obj = models.Contrats(
            uuid = str(uuid.uuid4()),
            user_uuid = obj_in.user_uuid,
            title = obj_in.title,
            clauses = obj_in.clauses,
            added_by = added_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    @classmethod
    def update(cls,db:Session,obj_in:schemas.ContratUpdate,added_by:str) -> Optional[models.Contrats]:
        db_obj = cls.get_by_uuid(db,obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="contrat-not-found")
        db_obj.user_uuid = obj_in.user_uuid if obj_in.user_uuid else db_obj.user_uuid
        db_obj.title = obj_in.title if obj_in.title else db_obj.title
        db_obj.clauses = obj_in.clauses if obj_in.clauses else db_obj.clauses
        db_obj.added_by = added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj



    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str) -> Optional[models.Contrats]:
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="contrat-not-found")
        db_obj.status = status
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str) -> Optional[models.Contrats]:
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="contrat-not-found")
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def delete(cls,db:Session,uuid:str) -> Optional[models.Contrats]:
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="contrat-not-found")
        db.delete(db_obj)
        db.commit()

    @classmethod
    def get_all_contrats(
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

        record_query = db.query(models.Contrats).filter(models.Contrats.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Contrats.title.ilike(f'%{keyword}%'),
                    models.Contrats.clauses.ilike(f'%{keyword}%')
                )
            )

        if status:
            record_query = record_query.filter(models.Contrats.status == status)

        if order and order_field and hasattr(models.Contrats, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Contrats, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Contrats, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.ContratsResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )

    @classmethod
    def get_contrats_by_added_by(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status: Optional[str] = None,
            added_by: Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Contrats).filter(models.Contrats.is_deleted == False,models.Contrats.added_by==added_by)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Contrats.title.ilike(f'%{keyword}%'),
                    models.Contrats.clauses.ilike(f'%{keyword}%')
                )
            )

        if status:
            record_query = record_query.filter(models.Contrats.status == status)

        if order and order_field and hasattr(models.Contrats, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Contrats, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Contrats, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.ContratsResponseListSlim1(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


contrats = CRUD_CONTRATS(models.Contrats)
