from sqlalchemy.orm import Session
from models.report import Report
from schemas.report import ReportCreate, ReportUpdate
from typing import List, Optional
from datetime import date
import uuid

def get_report(db: Session, report_id: str) -> Optional[Report]:
    return db.query(Report).filter(Report.id == report_id).first()

def get_reports(db: Session, skip: int = 0, limit: int = 100) -> List[Report]:
    return db.query(Report).offset(skip).limit(limit).all()

def create_report(db: Session, rp: ReportCreate) -> Report:
    db_rp = Report(
        id=str(uuid.uuid4()),
        title=rp.title,
        created_at=rp.created_at,
        content=rp.content,
        type=rp.type,
        value=rp.value
    )
    db.add(db_rp)
    db.commit()
    db.refresh(db_rp)
    return db_rp

def update_report(db: Session, report_id: str, rp: ReportUpdate) -> Optional[Report]:
    db_rp = get_report(db, report_id)
    if not db_rp:
        return None
    db_rp.title = rp.title
    db_rp.created_at = rp.created_at
    db_rp.content = rp.content
    db_rp.type = rp.type
    db_rp.value = rp.value
    db.commit()
    db.refresh(db_rp)
    return db_rp

def delete_report(db: Session, report_id: int) -> bool:
    db_rp = get_report(db, report_id)
    if not db_rp:
        return False
    db.delete(db_rp)
    db.commit()
    return True
