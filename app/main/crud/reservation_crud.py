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

class CRUDReservation(CRUDBase[models.Reservation,schemas.Reservation,schemas.ReservationUpdate]):

    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Reservation).filter(models.Reservation.uuid == uuid).first()
    
    def create(cls,db:Session,*,obj_in:schemas.ReservationCreate):
        new_address = models.Reservation(
            uuid = str(uuid.uuid4()),
            product_uuid= obj_in.product_uuid,
            status= obj_in.status,
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    

    def update(cls,db:Session,*,obj_in:schemas.ReservationUpdate):
        reservation = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if reservation is None:
            raise HTTPException(status_code=404, detail=__("key=reservation-not-found"))
        uuid = obj_in.uuid if obj_in.uuid else uuid
        product_uuid = obj_in.product_uuid if obj_in.product_uuid else product_uuid
        status = obj_in.status if obj_in.status else status
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    