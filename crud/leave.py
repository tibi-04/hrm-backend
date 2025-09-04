from sqlalchemy.orm import Session
from models.leave import Leave
from schemas.leave import LeaveCreate, LeaveUpdate
from typing import List, Optional
from datetime import date
from fastapi import HTTPException
import uuid

def get_leave(db: Session, leave_id: str) -> Optional[Leave]:
    return db.query(Leave).filter(Leave.id == leave_id).first()

def get_leaves(db: Session, skip: int = 0, limit: int = 100) -> List[Leave]:
    return db.query(Leave).offset(skip).limit(limit).all()

def create_leave(db: Session, lv: LeaveCreate) -> Leave:
    if lv.end_date < lv.start_date:
        raise HTTPException(status_code=400, detail="End date must be after or equal to start date.")
    db_lv = Leave(
        id=str(uuid.uuid4()),
        employee_id=lv.employee_id, 
        start_date=lv.start_date,
        end_date=lv.end_date,
        reason=lv.reason,
        status=lv.status
    )
    db.add(db_lv)
    db.commit()
    db.refresh(db_lv)
    return db_lv

def update_leave(db: Session, leave_id: str, lv: LeaveUpdate) -> Optional[Leave]:
    db_lv = get_leave(db, leave_id)
    if not db_lv:
        return None
    if lv.end_date < lv.start_date:
        raise HTTPException(status_code=400, detail="End date must be after or equal to start date.")
    db_lv.employee_id = lv.employee_id  
    db_lv.start_date = lv.start_date
    db_lv.end_date = lv.end_date
    db_lv.reason = lv.reason
    db_lv.status = lv.status
    db.commit()
    db.refresh(db_lv)
    return db_lv

def delete_leave(db: Session, leave_id: int) -> bool:
    db_lv = get_leave(db, leave_id)
    if not db_lv:
        return False
    db.delete(db_lv)
    db.commit()
    return True
