import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session

from app.main.core.mail import send_owner_message_for_new_reservation
from app.main.core.security import generate_password, get_password_hash
from app.main.crud import address
from app.main.crud.base import CRUDBase
from app.main import models,schemas



class CRUD_RESERVATION(CRUDBase[models.Reservation,schemas.ReservationResponse,schemas.ReservationCreate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str)->Optional[models.Reservation]:
        return db.query(models.Reservation).filter(models.Reservation.uuid == uuid,models.Reservation.is_deleted==False).first()


    @classmethod
    def create(cls,db:Session,obj_in:schemas.ReservationCreate) -> Optional[models.Reservation]:
        commond_uuid = str(uuid.uuid4())
        password: str = generate_password(8, 8)
        print(f"User password: {password}")

        new_user = models.User(
            uuid = commond_uuid,
            first_name= obj_in.full_name,
            last_name= obj_in.full_name,
            email = f"{obj_in.full_name}@gmail.com",
            role = models.UserRole.USER,
            password_hash=get_password_hash(password),
            phone_number=obj_in.phone_number,
        )
        db.add(new_user)
        db.commit()

        new_reservation = models.Reservation(
            uuid = str(uuid.uuid4()),
            product_uuid = obj_in.product_uuid,
            user_uuid=commond_uuid,
            message = obj_in.message
        )
        db.add(new_reservation)
        db.commit()

        product = db.query(models.Product).filter(models.Product.uuid == obj_in.product_uuid).first()
        if not product:
            raise HTTPException(status_code=404, detail=__(key="product-not-found"))

        owner = db.query(models.User).filter(models.User.uuid == product.owner_uuid).first()

        if owner and owner.email:
            send_owner_message_for_new_reservation(
                email_to=owner.email,
                full_name=obj_in.full_name,
                message=obj_in.message,
                code=product.code
            )

        return new_reservation


    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str) -> Optional[models.Reservation]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="reservation-not-found"))
        db_obj.status = status
        db.commit()


    @classmethod
    def delete(cls,db:Session,uuid:str) -> Optional[models.Reservation]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="reservation-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str) -> Optional[models.Reservation]:
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="reservation-not-found"))
        db_obj.is_deleted = True
        db.commit()



    @classmethod
    def get_all_reservation(
            cls,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            status:Optional[str] = None,
    ):
        record_query = db.query(models.Reservation).filter(models.Reservation.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Reservation.message.ilike(f'%{keyword}%')
                )
            )

        if status:
            record_query = record_query.filter(models.Reservation.status == status)

        if order and order_field and hasattr(models.Reservation, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Reservation, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Reservation, order_field).desc())

        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.ReservationResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query,
        )



reservations = CRUD_RESERVATION(models.Reservation)













