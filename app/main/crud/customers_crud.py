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
from app.main.crud.base import CRUDBase
from app.main import models,schemas
from app.main.core.security import get_password_hash, verify_password, generate_code


class CustomerCRUD(CRUDBase[models.Customer, schemas.CustomerCreate, schemas.CustomerUpdate]):

    @classmethod
    def get_by_email(cls,db:Session, email: str) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.email == email,models.Customer.is_deleted==False).first()

    @classmethod
    def get_by_uuid(cls,db:Session, uuid: str) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.uuid == uuid,models.Customer.is_deleted==False).first()

    @classmethod
    def get_by_phone_number(cls,db:Session, phone_number: str) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.phone_number == phone_number,models.Customer.is_deleted==False).first()

    @classmethod
    def get_by_phone_number_2(cls,db:Session, phone_number_2: str) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.phone_number_2 == phone_number_2,models.Customer.is_deleted==False).first()

    @classmethod
    def get_code_validation_by_uuid(cls,db:Session, uuid: str) -> Optional[models.ValidationAccount]:
        return db.query(models.ValidationAccount).filter(models.ValidationAccount.uuid == uuid,models.ValidationAccount.is_deleted==False).first()


    @classmethod
    def get_code_validation_by_email(cls,db:Session, email: str) -> Optional[models.ValidationAccount]:
        return db.query(models.ValidationAccount).filter(models.ValidationAccount.email == email,models.ValidationAccount.is_deleted == False).first()


    @classmethod
    def create(cls,db:Session, obj_in: schemas.CustomerCreate) -> Optional[models.Customer]:
        commun_uuid = str(uuid.uuid4())

        new_customer = models.Customer(
            uuid = commun_uuid,
            email = obj_in.email,
            phone_number = obj_in.phone_number,
            phone_number_2 = obj_in.phone_number_2,
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            country_uuid = obj_in.country_uuid,
            city_uuid = obj_in.city_uuid,
            password = get_password_hash(obj_in.password)
        )
        db.add(new_customer)
        db.commit()

        new_user = models.User(
            uuid = commun_uuid,
            first_name = obj_in.first_name,
            email = obj_in.email,
            last_name = obj_in.last_name,
            phone_number = obj_in.phone_number,
            password_hash= get_password_hash(obj_in.password),
            role = models.UserRole.CUSTOMER,
            status = models.UserStatus.UNACTIVED
        )
        db.add(new_user)
        db.commit()

        code = generate_code(length=12)
        code = str(code[0:6])

        account_validation = models.ValidationAccount(
            uuid = str(uuid.uuid4()),
            code = code,
            email = obj_in.email,
            expirat_at= datetime.utcnow() + timedelta(hours=24)
        )
        db.add(account_validation)
        db.commit()
        send_code_validation(
            email_to=obj_in.email,
            code=code,
            expirat_at=account_validation.expirat_at,
            full_name= f"{obj_in.first_name} {obj_in.last_name}"
        )
        return new_customer

    @classmethod
    def verify_account(cls,db:Session,code:str,email:str):
        db_obj = cls.get_code_validation_by_email(db=db,email=email)
        if not db_obj:
                raise HTTPException(status_code=404, detail=__(key="email-not-found"))
        if db_obj.email != email:
            raise HTTPException(status_code=400, detail=__(key="email-invalid"))
        if db_obj.code != code:
            raise HTTPException(status_code=400, detail=__(key="code-invalid"))
        if db_obj.is_used:
            raise HTTPException(status_code=400, detail=__(key="otp-used"))
        if db_obj.expirat_at < datetime.now():
            raise HTTPException(status_code=400, detail=__(key="otp-expired"))
        db_obj.is_used = True

        customer = cls.get_by_email(db=db, email=email)
        if not customer:
            raise HTTPException(status_code=404, detail=__(key="customer-email-not-found"))
        customer.status = models.Customer_Status.active

        # Activer le compte User correspondant
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail=__(key="user-email-not-found"))
        user.status = models.UserStatus.ACTIVED

        db.commit()

    @classmethod
    def delete(cls,db:Session,uuid:str):
        obj_in  = cls.get_by_uuid(db=db,uuid=uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="customer-not-found"))
        db.delete(obj_in)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db=db,uuid=uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="customer-not-found"))
        obj_in.is_deleted = True
        db.commit()

    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        obj_in = cls.get_by_uuid(db=db,uuid=uuid)
        if not obj_in:
            raise HTTPException(status_code=404, detail=__(key="customer-not-found"))
        obj_in.status = status
        db.commit()
     
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
    ):
        if page < 1:
            page = 1
        
        record_query = db.query(models.Customer).filter(models.Customer.is_deleted == False)

        if keyword:
            record_query = db.record_query.filter(
                or_(
                    models.Customer.first_name.ilike(f'%{keyword}%'),
                    models.Customer.last_name.ilike(f'%{keyword}%'),
                    models.Customer.email.ilike(f'%{keyword}%'),
                    models.Customer.phone_number.ilike(f'%{keyword}%'),
                    models.Customer.phone_number_2.ilike(f'%{keyword}%'),
                )
            )

        if status:
            record_query = record_query.filter(models.Customer.status == status)

        if order and order_field and hasattr(models.Experience, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Customer, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Customer, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CustomerResponseList(
            total = total,
            pages = math.ceil(total / per_page),
            per_page = per_page,
            current_page = page,
            data = record_query
        )
    

customers = CustomerCRUD(models.Customer)